from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializer import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .ai_engine import analyze_message  
# Create your views here.
@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "username": user.username,
                "email": user.email
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
def chatbot_response(request):

    if request.method == "POST":

        try:
            data = json.loads(request.body)
            message = data.get("message")

            if not message:
                return JsonResponse({"error": "Message is required"}, status=400)

            result = analyze_message(message)

            return JsonResponse({
                "response": result["response"],
                "emotion": result["emotion"],
                "is_safety_alert": result["is_safety_alert"]
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)