from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class UserBaseSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)


class UserCreateSerializer(UserBaseSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate_password(self, value):
        # Will raise ValidationError if the password is not invalid.
        validate_password(value)

        # Password is still in plaintext.
        return value


class UserUpdateSerializer(UserBaseSerializer):
    pass


class UserDetailSerializer(UserBaseSerializer):
    email = serializers.EmailField(max_length=255)
