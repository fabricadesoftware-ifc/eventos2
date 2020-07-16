from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from eventos2.core.models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):  # pragma: no cover - no complexity
        raise NotImplementedError("Use ActivityCreateSerializer")

    class Meta:
        model = User
        fields = ["public_id", "first_name", "last_name", "email"]
        extra_kwargs = {"public_id": {"read_only": True}, "email": {"read_only": True}}


class UserCreateSerializer(serializers.ModelSerializer):
    def validate_password(self, value):
        # Will raise ValidationError if the password is not invalid.
        validate_password(value)

        # Password is still in plaintext.
        return value

    def create(self, validated_data):
        user = User(email=validated_data["email"], username=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ["public_id", "first_name", "last_name", "email", "password"]
        extra_kwargs = {
            "public_id": {"read_only": True},
            "password": {"write_only": True},
        }
