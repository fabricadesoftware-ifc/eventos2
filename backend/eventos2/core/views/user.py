from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from eventos2.core.serializers import (
    UserCreateSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
)
from eventos2.core.services import user as user_service


class UserViewSet(ViewSet):
    @swagger_auto_schema(
        request_body=UserCreateSerializer,
        responses={200: UserDetailSerializer, 400: "Validation error"},
    )
    def create(self, request):
        in_serializer = UserCreateSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data

        user = user_service.create(**data)

        out_serializer = UserDetailSerializer(user)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False, url_path="current",
    )
    @swagger_auto_schema(responses={200: UserDetailSerializer})
    def current(self, request):
        if not (request.user and request.user.is_authenticated):
            raise PermissionDenied()
        user = user_service.get_by_id(self.request.user.pk, must_be_active=True)
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

        user = user_service.update(actor=request.user, user_id=request.user.pk, **data)

        out_serializer = UserDetailSerializer(user)
        return Response(out_serializer.data)

    @current.mapping.delete
    @swagger_auto_schema(responses={204: "Success"})
    def current_destroy(self, request):
        if not (request.user and request.user.is_authenticated):
            raise PermissionDenied()

        user_service.delete(actor=request.user, user_id=request.user.pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
