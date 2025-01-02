from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.conf import settings
from rest_framework import generics
from .serializers import UserRegistrationSerializer, UserLoginSerializer

# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=400)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        response = Response()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                csrf_token = csrf.get_token(request)
                response = Response({
                    'message': 'Login Successful',
                    'access_token': access_token,
                    'csrf_token': csrf_token,
                })
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,
                    secure=True,
                    samesite='Lax',
                    max_age=86400,
                )
                return response
            else:
                return Response({'No active':'This account is not active'}, status=401)
        else:
            return Response({'Invalid': 'Invalid credientials'}, status=401)
    
class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token not found'}, status=401)
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token})
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=401)
        
class LogoutView(APIView):
    def post(self, request):
        response = Response({'message': 'Logout Successful'})
        response.delete_cookie('refresh_token')
        return response