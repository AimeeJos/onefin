"""Serializers"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    
    access_token = serializers.CharField(max_length=100, read_only=True)
    
    class Meta:
        model = User
        fields = ["username", "password", "access_token"]
        
    
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User.objects.create(**validated_data) 
        user.set_password(password)
        user.save()
        username = validated_data.get("username", None)
        
        user = auth.authenticate(username=username, password=password)  
        resp = {
            'username': user.username,
            'email': user.email,
            'access_token': user.tokens['access'],
            'refresh_token': user.tokens['refresh'],
            }

        return resp


class LoginSerializer(serializers.Serializer):
    """Login serializer"""
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50, write_only=True)
    email = serializers.EmailField(read_only=True)
    user_type = serializers.CharField(max_length=100, read_only=True)
    access_token = serializers.CharField(max_length=100, read_only=True)
    refresh_token = serializers.CharField(max_length=100, read_only=True)
    
    class Meta:
        model = User
        fields = "__all__"
        
    def validate(self, validated_data):
        password = validated_data.pop("password", None)
        username = validated_data.pop("username", None)
        
        user = auth.authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed(
                {'error': 'Invalid username & password'})

        resp = {
            'username': user.username,
            'email': user.email,
            'access_token': user.tokens['access'],
            'refresh_token': user.tokens['refresh'],
            }

        return resp