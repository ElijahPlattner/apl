from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
import subprocess
import tempfile
from pathlib import Path
import os
import json, re
from api.pdf_analyzer import analyze_pdf




@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello from Django!"})

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class AnalyzePDFView(APIView):
    def post(self, request):
        # ✅ Require a file upload
        if 'file' not in request.FILES:
            return Response({"error": "Please upload a PDF file."}, status=400)

        pdf_file = request.FILES['file']

        # ✅ Save uploaded PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            for chunk in pdf_file.chunks():
                tmp_pdf.write(chunk)
            tmp_pdf_path = tmp_pdf.name

        try:
            # ✅ Run analysis directly (in-process, uses shared word_cache)
            print(f"Running in-process PDF analysis for: {tmp_pdf_path}")
            result = analyze_pdf(tmp_pdf_path)

            # Clean up temporary file
            os.remove(tmp_pdf_path)

            # ✅ Return structured results
            return Response({
                "message": "PDF analyzed successfully.",
                "counts": result.get("counts", {}),
                "caps_words": result.get("caps_words", []),
                "uncommon_words": result.get("uncommon_words", []),
                "unknown_words": result.get("unknown_words", []),
                "looked_up_words": result.get("looked_up_words", []),
            })

        except Exception as e:
            # Always clean up temporary file on failure
            if os.path.exists(tmp_pdf_path):
                os.remove(tmp_pdf_path)
            return Response({"error": str(e)}, status=500)