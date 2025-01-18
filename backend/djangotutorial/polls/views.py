from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny 
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class RegisterUser(APIView):
    # No authentication required for registration
    permission_classes = [AllowAny] # Allow all users to access

    def post(self, request, *args, **kwargs):
        print("Request user:", request.user)
        print("Request data:", request.data)
        print("Received data:", request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)