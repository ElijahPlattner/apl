from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.models import User
from api.models import Analyzation
from .serializers import RegisterSerializer
from .serializers import AnalyzationSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
import subprocess
import tempfile
from pathlib import Path
import time
import os
import json, re
from api.pdf_analyzer import analyze_pdf



@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello from Django!"})


def save_analysis_to_file(result, output_dir):
    """
    Save the full word classification results to a fast, minimal text file.

    Returns:
        The full path to the written file.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Use timestamp or unique ID for filename
    filename = f"analysis_{int(time.time())}.apl"
    output_path = Path(output_dir) / filename

    # Open in write mode (no compression yet — fastest)
    with open(output_path, "w", encoding="utf-8") as f:
        # Write each category sequentially for locality
        for w in result.get("caps_words", []):
            f.write(f"{w}|caps\n")
        for w in result.get("uncommon_words", []):
            f.write(f"{w}|uncommon\n")
        for w in result.get("unknown_words", []):
            f.write(f"{w}|unknown\n")
        for w in result.get("looked_up_words", []):
            f.write(f"{w}|looked_up\n")

    return str(output_path)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class AnalyzePDFView(APIView):
    def post(self, request):
        # Require file
        if 'file' not in request.FILES:
            return Response({"error": "Please upload a PDF file."}, status=400)

        # Require user_id
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "Please provide user_id in the request."}, status=400)
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return Response({"error": "user_id must be an integer."}, status=400)

        # Validate user exists
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        pdf_file = request.FILES['file']

        # Save uploaded PDF temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            for chunk in pdf_file.chunks():
                tmp_pdf.write(chunk)
            tmp_pdf_path = tmp_pdf.name

        try:
            print(f"Running in-process PDF analysis for: {tmp_pdf_path} (user_id={user_id})")
            result = analyze_pdf(tmp_pdf_path)

            # Expected result keys (based on your file-saver):
            #   caps_words, uncommon_words, unknown_words, looked_up_words, counts, etc.
            base_dir = Path(__file__).resolve().parent.parent
            output_dir = base_dir / "analyzed_outputs" / f"user_{user_id}"

            output_file = save_analysis_to_file(result, output_dir=str(output_dir.resolve()))
            output_name = Path(output_file).name

            counts = result.get("counts", {})

            analyzation = Analyzation.objects.create(
                user=user,
                caps_count=counts.get("caps", len(result.get("caps_words", []))),
                uncommon_count=counts.get("uncommon", len(result.get("uncommon_words", []))),
                unknown_count=counts.get("unknown", len(result.get("unknown_words", []))),
                looked_up_count=counts.get("looked_up", len(result.get("looked_up_words", []))),
                file_name=output_name,
                file_path=str(output_file),
                payment_id=0,
            )

            os.remove(tmp_pdf_path)

            return Response({
                "message": "PDF analyzed successfully.",
                "user_id": user_id,
                "username": user.username,
                "analyzation_id": analyzation.id,
                "counts": counts,
                "word_lists": {
                    "caps": result.get("caps_words", []),
                    "uncommon": result.get("uncommon_words", []),
                    "unknown": result.get("unknown_words", []),
                    "looked_up": result.get("looked_up_words", []),
                },
                "output_file": str(output_file),
            })

        except Exception as e:
            if os.path.exists(tmp_pdf_path):
                os.remove(tmp_pdf_path)
            return Response({"error": str(e)}, status=500)

class UserAnalyzationHistoryView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = AnalyzationSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Analyzation.objects.filter(user__id=user_id).order_by('-created_at')

class AnalyzationDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = AnalyzationSerializer
    queryset = Analyzation.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'analyzation_id'

    def retrieve(self, request, *args, **kwargs):
        analyzation = self.get_object()

        # Parse the .apl file from disk
        file_path = analyzation.file_path
        if not os.path.exists(file_path):
            return Response({"error": f"Analysis file not found at {file_path}"}, status=404)

        word_lists = {
            "caps": [],
            "uncommon": [],
            "unknown": [],
            "looked_up": [],
        }

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    # Each line looks like: word|category
                    parts = line.strip().split("|")
                    if len(parts) == 2:
                        word, category = parts
                        if category in word_lists:
                            word_lists[category].append(word)

            # Compute counts from lists (for consistency with AnalyzePDFView)
            counts = {
                "caps": len(word_lists["caps"]),
                "uncommon": len(word_lists["uncommon"]),
                "unknown": len(word_lists["unknown"]),
                "looked_up": len(word_lists["looked_up"]),
            }

            return Response({
                "message": "Analyzation loaded successfully.",
                "analyzation_id": analyzation.id,
                "user_id": analyzation.user.id if analyzation.user else None,
                "username": analyzation.user.username if analyzation.user else None,
                "counts": counts,
                "word_lists": word_lists,
                "file_name": analyzation.file_name,
                "file_path": analyzation.file_path,
                "created_at": analyzation.created_at,
                "modified_at": analyzation.modified_at,
            })

        except Exception as e:
            return Response({"error": f"Failed to parse file: {str(e)}"}, status=500)