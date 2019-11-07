from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, validators

from eventos2.core.models import User


class UserBaseSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=255,
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all(), message="Este email já foi utilizado."
            )
        ],
    )
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)


class UserCreateSerializer(UserBaseSerializer):
    password = serializers.CharField(max_length=255)

    def validate_password(self, value):
        if validate_password(value) is not None:
            raise serializers.ValidationError("Invalid password")
        return make_password(value)

    def create(self, validated_data):
        return User.objects.create(**validated_data, username=validated_data["email"])


class UserUpdateSerializer(UserBaseSerializer):
    email = serializers.EmailField(max_length=255, read_only=True)

    def update(self, user, validated_data):
        for k, v in validated_data.items():
            setattr(user, k, v)
        user.save()
        return user


class UserDetailSerializer(UserBaseSerializer):
    pass
