from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password1', 'password2', 'email']

    #Function to validate passwords
    def validate(self, data):
        print(f"Incoming data: {data}")
        if data.get('password1') != data.get('password2'):
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        
        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})
        
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        
        return data
    
        
    
    #Save password as a hash
    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password1']
        email = validated_data['email']
        return User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    