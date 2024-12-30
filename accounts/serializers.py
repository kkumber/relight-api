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
    
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return data
    
    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password1']
        email = validated_data['email']
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return User
    

