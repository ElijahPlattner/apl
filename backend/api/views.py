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
            # Run the analyzer
            result = subprocess.run(
                ["python3", str(analyzer_script), tmp_pdf_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            os.remove(tmp_pdf_path)

            if result.returncode != 0:
                return Response({"error": result.stderr.strip()}, status=500)

            # Extract JSON from stdout (ignores print statements before it)
            stdout_text = result.stdout.strip()

            match = re.search(r'\{.*\}', stdout_text, re.DOTALL)
            if not match:
                return Response({
                    "error": "No JSON output found from analyzer.",
                    "raw_output": stdout_text
                }, status=500)

            json_str = match.group(0)
            try:
                analysis_output = json.loads(json_str)
            except json.JSONDecodeError:
                return Response({
                    "error": "Invalid JSON format from analyzer.",
                    "raw_output": stdout_text
                }, status=500)

            # Now you can access word lists directly
            caps_list = analysis_output.get("caps_words", [])
            uncommon_list = analysis_output.get("uncommon_words", [])
            unknown_list = analysis_output.get("unknown_words", [])

            return Response({
                "message": "PDF analyzed successfully.",
                "caps_words": caps_list,
                "uncommon_words": uncommon_list,
                "unknown_words": unknown_list,
            })

        except subprocess.TimeoutExpired:
            os.remove(tmp_pdf_path)
            return Response({"error": "Analysis timed out."}, status=500)
        except Exception as e:
            os.remove(tmp_pdf_path)
            return Response({"error": str(e)}, status=500)