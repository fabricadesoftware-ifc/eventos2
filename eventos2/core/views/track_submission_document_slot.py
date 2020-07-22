from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from eventos2.core.models import TrackSubmissionDocumentSlot
from eventos2.core.serializers import (
    TrackSubmissionDocumentSlotCreateSerializer,
    TrackSubmissionDocumentSlotSerializer,
)
from eventos2.utils.permissions import PerActionPermissions
from eventos2.utils.viewsets import CUDViewSet


class TrackSubmissionDocumentSlotViewSet(CUDViewSet):
    queryset = TrackSubmissionDocumentSlot.objects.all()
    permission_classes = [PerActionPermissions]
    per_action_permissions = {
        "create": "core.change_event",
        "update": "core.change_event",
        "destroy": "core.change_event",
    }

    def get_serializer_class(self):
        if self.action == "create":
            return TrackSubmissionDocumentSlotCreateSerializer
        return TrackSubmissionDocumentSlotSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        track = serializer.validated_data["track"]
        if not request.user.has_perm("core.change_event", track.event):
            raise PermissionDenied(
                "You're not allowed to add a slot to a track in this event."
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
