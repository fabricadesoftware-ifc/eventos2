from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from eventos2.core.models import User
from eventos2.core.serializers import (
    UserCreateSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
)


class UserViewSet(ViewSet):
    @swagger_auto_schema(
        request_body=UserCreateSerializer,
        responses={200: UserDetailSerializer, 400: "Validation error"},
    )
    def create(self, request):
        in_serializer = UserCreateSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data

        if User.objects.filter(email=data["email"]).exists():
            raise ValidationError("Email already used.")

        user = User.objects.create(
            email=data["email"],
            username=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )
        user.set_password(data["password"])
        user.save()

        out_serializer = UserDetailSerializer(user)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False, url_path="current",
    )
    @swagger_auto_schema(responses={200: UserDetailSerializer})
    def current(self, request):
        if not (request.user and request.user.is_authenticated):
            raise PermissionDenied()
        user = User.objects.filter(is_active=True).get(pk=request.user.pk)
        return Response(UserDetailSerializer(user).data)

    @current.mapping.put
    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        responses={200: UserDetailSerializer, 400: "Validation error"},
    )
    def current_update(self, request):
        if not (request.user and request.user.is_authenticated):
            raise PermissionDenied()

        in_serializer = UserUpdateSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data

        user = User.objects.filter().get(pk=request.user.pk)

        if not request.user.has_perm("core.change_user", user):
            raise PermissionDenied("Not authorized to edit this user.")

        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.save()

        out_serializer = UserDetailSerializer(user)
        return Response(out_serializer.data)

    @current.mapping.delete
    @swagger_auto_schema(responses={204: "Success"})
    def current_destroy(self, request):
        if not (request.user and request.user.is_authenticated):
            raise PermissionDenied()

        user = User.objects.filter().get(pk=request.user.pk)
        if not request.user.has_perm("core.delete_user", user):
            raise PermissionDenied("Not authorized to delete this user.")

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
