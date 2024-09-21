from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from google.oauth2 import id_token
from google.auth.transport import requests
from Account.models import User


@api_view(["POST"])
def main_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful'})
    return JsonResponse({'error': 'Invalid Email or Password'}, status=400)


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
            'id' : user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'authenticated':True
        }
        return Response(user_data)
    else:
        return Response({'authenticated': False})


@api_view(["POST"])
def login_with_google(request):
    token = request.data.get("token")
    if not token:
        return JsonResponse({"error": "Token is missing"}, status=400)
    credential = token.get("credential")
    clientId = token.get("clientId")
    try:
        idinfo = id_token.verify_oauth2_token(
            credential, requests.Request(), clientId)
        email = idinfo.get('email')
        name = idinfo.get('name')
        user, created = User.objects.get_or_create(
            email=email, defaults={'username': name})
        login(request, user)

        return JsonResponse({"message": "Login successful", "user": {"email": user.email, "username": user.username}})

    except ValueError:
        return JsonResponse({"error": "Invalid token"}, status=400)
