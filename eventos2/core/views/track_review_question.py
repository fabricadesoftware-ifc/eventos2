from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from eventos2.core.models import TrackReviewQuestion
from eventos2.core.serializers import (
    TrackReviewQuestionCreateSerializer,
    TrackReviewQuestionSerializer,
)
from eventos2.utils.permissions import PerActionPermissions
from eventos2.utils.viewsets import CUDViewSet


class TrackReviewQuestionViewSet(CUDViewSet):
    queryset = TrackReviewQuestion.objects.all()
    permission_classes = [PerActionPermissions]
    per_action_permissions = {
        "create": "core.change_event",
        "update": "core.change_event",
        "destroy": "core.change_event",
    }

    def get_serializer_class(self):
        if self.action == "create":
            return TrackReviewQuestionCreateSerializer
        return TrackReviewQuestionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        track = serializer.validated_data["track"]
        if not request.user.has_perm("core.change_event", track.event):
            raise PermissionDenied(
                "You're not allowed to add a review question to a track in this event."
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
