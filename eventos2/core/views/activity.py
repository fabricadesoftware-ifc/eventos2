from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from eventos2.core.models import Activity
from eventos2.core.serializers import (
    ActivityCreateSerializer,
    ActivityRegistrationUserListSerializer,
    ActivitySerializer,
)
from eventos2.utils.permissions import PerActionPermissions
from eventos2.utils.viewsets import CRUDViewSet


class ActivityViewSet(CRUDViewSet):
    lookup_field = "slug"
    queryset = Activity.available_objects.all()
    permission_classes = [PerActionPermissions]
    per_action_permissions = {
        "create": "core.change_event",
        "retrieve": "core.view_activities_for_event",
        "update": "core.change_event",
        "destroy": "core.change_event",
        "list_registrations": "core.view_registrations_for_activity",
    }

    def get_serializer_class(self):
        if self.action == "create":
            return ActivityCreateSerializer
        return ActivitySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event = serializer.validated_data["event"]
        if not request.user.has_perm("core.change_event", event):
            raise PermissionDenied(
                "You're not allowed to add an activity to this event."
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses={200: ActivityRegistrationUserListSerializer(many=True)})
    @action(detail=True, url_path="registrations", url_name="list-registrations")
    def list_registrations(self, request, slug=None):
        activity = self.get_object()
        serializer = ActivityRegistrationUserListSerializer(
            activity.registrations, many=True
        )
        return Response(serializer.data)
