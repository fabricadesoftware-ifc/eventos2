from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
        read_only_fields = ["email"]


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)

    def validate_password(self, value):
        if validate_password(value) is not None:
            raise serializers.ValidationError("Invalid password")
        return make_password(value)

    def create(self, validated_data):
        return User.objects.create(**validated_data, username=validated_data["email"])
