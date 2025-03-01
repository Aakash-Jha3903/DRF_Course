import django.contrib.auth
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

    def validate(self, values):
        if User.objects.filter(username=values["username"]).exists():
            raise serializers.ValidationError("Username already exists")
        return values

    def create(self, validated_values):
        user = User.objects.create_user(username=validated_values["username"].lower())
        user.set_password(validated_values["password"])
        return validated_values


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

    def validate(self, values):
        if not User.objects.filter(username=values["username"]).exists():
            raise serializers.ValidationError("Username does not exists, with these Credentials !")
        return values

    def get_jwt_token(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        # print(user)
        if not user:    
            return {"message": "Invalid Credentials", }
        refresh = RefreshToken.for_user(user)
        return {
            "message": "Login successfully",
            "data": {
                "token": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            },
        }
