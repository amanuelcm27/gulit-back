from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from google.oauth2 import id_token
# from google.auth.transport import requests
from Account.models import User
from .serializers import *
from .serializers import UserRegisterSerializer
import requests
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


@api_view(["POST"])
def main_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful'})
    return Response({'error': 'Invalid Email or Password'}, status=400)


@api_view(["POST"])
def logout_user(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})


@api_view(["GET"])
def csrf_token_view(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})


@api_view(['GET'])
def get_logged_in_user(request):

    if request.user.is_authenticated:

        user = request.user
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'authenticated': True
        }
        return Response(user_data)
    else:
        return Response({'authenticated': False})


@api_view(["POST"])
def login_with_google(request):
    token = request.data.get("token")

    access_token = token.get("access_token")
    if not token:
        return JsonResponse({"error": "Access token is missing"}, status=400)

    google_user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    params = {"access_token": access_token}

    try:
        user_info_response = requests.get(google_user_info_url, params=params )
        user_info = user_info_response.json()
        if user_info_response.status_code != 200:
            return JsonResponse({"error": "Invalid access token"}, status=400)
        email = user_info.get("email")
        name = user_info.get("name")
        if not email or not name:
            return JsonResponse({"error": "Invalid user info"}, status=400)
        user, created = User.objects.get_or_create(
            email=email, defaults={'username': name})
        login(request, user)
        return JsonResponse({
            "message": "Login successful",
            "user": {"email": user.email, "username": user.username}
        })

    except ValueError:
        return JsonResponse({"error": "Invalid token"}, status=400)


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data.get("registerInfo"))

    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        return Response({"success": "User registered successfully"}, status=201)

    return Response(serializer.errors, status=400)


class SetUserRoleView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

