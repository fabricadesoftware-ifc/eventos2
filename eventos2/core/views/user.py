from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from eventos2.core.models import User
from eventos2.core.serializers import UserCreateSerializer, UserSerializer
from eventos2.utils.permissions import PerActionPermissions
from eventos2.utils.viewsets import CViewSet


class UserViewSet(CViewSet):
    queryset = User.objects.filter(is_active=True)
    permission_classes = [PerActionPermissions]
    per_action_permissions = {
        "create": PerActionPermissions.ALLOW_ANY,
        "current": PerActionPermissions.ALLOW_AUTHENTICATED,
        "current_update": PerActionPermissions.ALLOW_AUTHENTICATED,
        "current_destroy": PerActionPermissions.ALLOW_AUTHENTICATED,
    }

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    @action(
        detail=False, url_path="current",
    )
    def current(self, request):
        user = User.objects.filter(is_active=True).get(pk=request.user.pk)
        return Response(self.get_serializer(user).data)

    @current.mapping.put
    def current_update(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = User.objects.filter().get(pk=request.user.pk)

        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.save()

        return Response(serializer.data)

    @current.mapping.delete
    def current_destroy(self, request):
        user = User.objects.filter().get(pk=request.user.pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
