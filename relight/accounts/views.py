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
        # serialized data for validation
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=400)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        response = Response()
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                # Get a refresh token with user credentials
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                # Use csrf
                csrf_token = csrf.get_token(request)
                # Return a response with an access token so frontend can store it
                response = Response({
                    'message': 'Login Successful',
                    'access_token': access_token,
                    'csrf_token': csrf_token,
                })
                # Set the refresh token in an httponly cookie
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
        # Get the fresh token from cookies
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token not found'}, status=401)
        
        try:
            # Try to get another refresh token
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token}) # Return a new access token
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=401)
        
class LogoutView(APIView):
    def post(self, request):
        response = Response({'message': 'Logout Successful'})
        response.delete_cookie('refresh_token') # Delete refresh token from cookies on logout
        return response