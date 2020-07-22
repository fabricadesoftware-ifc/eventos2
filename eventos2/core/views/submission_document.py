from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from eventos2.core.models import SubmissionDocument
from eventos2.core.serializers import SubmissionDocumentSerializer
from eventos2.utils.permissions import PerActionPermissions
from eventos2.utils.viewsets import CViewSet


class SubmissionDocumentViewSet(CViewSet):
    queryset = SubmissionDocument.objects.all()
    serializer_class = SubmissionDocumentSerializer
    permission_classes = [PerActionPermissions]
    per_action_permissions = {"create": "core.change_submission"}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        submission = serializer.validated_data["submission"]
        if not request.user.has_perm("core.change_submission", submission):
            raise PermissionDenied(
                "You're not allowed to add a document to this submission."
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
