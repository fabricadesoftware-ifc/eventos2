from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from eventos2.core.models import Track
from eventos2.core.serializers import TrackCreateSerializer, TrackSerializer
from eventos2.utils.permissions import PerActionPermissions
from eventos2.utils.viewsets import CRUDViewSet


class TrackViewSet(CRUDViewSet):
    lookup_field = "slug"
    queryset = Track.available_objects.all()
    permission_classes = [PerActionPermissions]
    per_action_permissions = {
        "create": "core.change_event",
        "retrieve": "core.view_tracks_for_event",
        "update": "core.change_event",
        "destroy": "core.change_event",
    }

    def get_serializer_class(self):
        if self.action == "create":
            return TrackCreateSerializer
        return TrackSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event = serializer.validated_data["event"]
        if not request.user.has_perm("core.change_event", event):
            raise PermissionDenied("You're not allowed to add a track to this event.")

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
