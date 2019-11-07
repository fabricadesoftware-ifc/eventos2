from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from eventos2.core.models import User
from eventos2.core.serializers import (
    UserCreateSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
)


class UserViewSet(GenericViewSet):
    queryset = User.objects.filter(is_active=True)

    @swagger_auto_schema(
        request_body=UserCreateSerializer,
        responses={200: UserDetailSerializer, 400: "Validation error"},
    )
    def create(self, request):
        request_serializer = UserCreateSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        user = request_serializer.save()

        response_serializer = UserDetailSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        url_path="current",
        permission_classes=[permissions.IsAuthenticated],
    )
    @swagger_auto_schema(responses={200: UserDetailSerializer})
    def current(self, request):
        user = self.queryset.get(pk=self.request.user.pk)
        return Response(UserDetailSerializer(user).data)

    @current.mapping.put
    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        responses={200: UserDetailSerializer, 400: "Validation error"},
    )
    def current_update(self, request):
        user = self.queryset.get(pk=self.request.user.pk)
        request_serializer = UserUpdateSerializer(user, data=request.data)
        request_serializer.is_valid(raise_exception=True)
        request_serializer.save()

        response_serializer = UserDetailSerializer(user)
        return Response(response_serializer.data)

    @current.mapping.delete
    @swagger_auto_schema(responses={204: "Success"})
    def current_destroy(self, request):
        user = self.queryset.get(pk=self.request.user.pk)
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
