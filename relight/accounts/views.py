from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.conf import settings
from rest_framework import generics
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Register Successful',
                'user': serializer.data,
            })    
        return Response({'success': False, 'message': serializer.errors}, status=400)
       
        
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
            # Get a refresh token with user credentials
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            # Use csrf
            csrf_token = csrf.get_token(request)
            # Return a response with an access token so frontend can store it
            response = Response({
                'success': True,
                'message': 'Login Successful',
                'access_token': access_token,
                'csrf_token': csrf_token,
                'user': {'id': user.id, 'username': user.username},
            })
            # Set the refresh token in an httponly cookie
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='None',
                max_age=1209600,
            )
            return response
        else:
            return Response({'success': False ,'message': 'Invalid username or password'}, status=200)
        
    
@method_decorator(csrf_exempt, name='dispatch')    
class RefreshTokenView(APIView):
    def post(self, request):
        # Get the fresh token from cookies
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token not found'}, status=401)
        
        try:
            # Try to get another refresh token
            refresh = RefreshToken(refresh_token)
            user_id = refresh['user_id']

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=404)

            access_token = str(refresh.access_token)
            return Response({'access_token': access_token, 'user' : {'id': user.id, 'username': user.username}})
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=401)
        
        
class LogoutView(APIView):
    def post(self, request):
        token = request.COOKIES.get('refresh_token')
        try:
            RefreshToken(token).blacklist()
        except TokenError:
            pass
        response = Response({'message': 'Logout Successful'})
        response.delete_cookie('refresh_token') # Delete refresh token from  cookies on logout
        return response


class UserInfoView(APIView):
    def get(self, request):
        print(f"Request: {request.user}")
        return Response({'id': request.user.id, 'username': request.user.username})

