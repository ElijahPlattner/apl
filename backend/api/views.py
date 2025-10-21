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


@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello from Django!"})

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class AnalyzePDFView(APIView):
    def post(self, request):
        # Require a file upload
        if 'file' not in request.FILES:
            return Response({"error": "Please upload a PDF file."}, status=400)

        pdf_file = request.FILES['file']

        # Save uploaded PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            for chunk in pdf_file.chunks():
                tmp_pdf.write(chunk)
            tmp_pdf_path = tmp_pdf.name

        # Path to your analyzer script
        # analyzer_script = Path(__file__).resolve().parent.parent / "analyzer" / "analyze.py"
        analyzer_script = Path(__file__).resolve().parent.parent / "analyzer" / "analyze.py"
        try:
            print("Running analyzer at:", analyzer_script)
            # Run the analyzer as a subprocess
            result = subprocess.run(
                ["python3", str(analyzer_script), tmp_pdf_path],
                capture_output=True,
                text=True,
                timeout=60
            )

            # Remove the temp file
            os.remove(tmp_pdf_path)

            # Check for errors
            if result.returncode != 0:
                return Response(
                    {"error": result.stderr.strip() or "Analyzer failed."},
                    status=500
                )

            # The analyzer prints results to stdout, so return that
            return Response({
                "message": "PDF analyzed successfully.",
                "output": result.stdout
            })

        except subprocess.TimeoutExpired:
            os.remove(tmp_pdf_path)
            return Response({"error": "Analysis timed out."}, status=500)
        except Exception as e:
            os.remove(tmp_pdf_path)
            return Response({"error": str(e)}, status=500)