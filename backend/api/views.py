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

        # Require user_id in POST data
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

            # Get absolute path to the analyzed_outputs folder (one level up)
            base_dir = Path(__file__).resolve().parent.parent  # adjust .parent depth if needed
            output_dir = base_dir / "analyzed_outputs" / f"user_{user_id}"

            # Save result file and get its absolute path
            output_file = save_analysis_to_file(result, output_dir=str(output_dir.resolve()))
            output_name = Path(output_file).name

            # Parse counts safely
            counts = result.get("counts", {})
            caps = counts.get("caps", 0)
            common = counts.get("common", 0)
            uncommon = counts.get("uncommon", 0)
            unknown = counts.get("unknown", 0)
            looked_up = counts.get("looked_up", 0)
            skip = counts.get("skip", 0)

            # Save to DB
            analyzation = Analyzation.objects.create(
                user=user,
                caps_count=caps,
                common_count=common,
                uncommon_count=uncommon,
                unknown_count=unknown,
                looked_up_count=looked_up,
                skip_count=skip,
                file_name=output_name,
                file_path=str(output_file),
                payment_id=0,  # placeholder if not applicable yet
            )

            # Clean up tmp file
            os.remove(tmp_pdf_path)

            return Response({
                "message": "PDF analyzed successfully.",
                "user_id": user_id,
                "username": user.username,
                "analyzation_id": analyzation.id,
                "counts": counts,
                "output_file": output_file,
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