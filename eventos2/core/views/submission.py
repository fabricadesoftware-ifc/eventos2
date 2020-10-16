from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from eventos2.core.serializers import (
    SubmissionCreateSerializer,
    SubmissionDetailSerializer,
)


class SubmissionViewSet(ViewSet):
    @extend_schema(
        request=SubmissionCreateSerializer, responses={200: SubmissionDetailSerializer}
    )
    def create(self, request):
        in_serializer = SubmissionCreateSerializer(
            data=request.data, context={"author": request.user}
        )
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data

        track = data["track"]

        if not request.user.has_perm("core.add_submission_to_track", track):
            raise PermissionDenied("You're not authorized to submit to this track.")

        submission = in_serializer.save()

        out_serializer = SubmissionDetailSerializer(submission)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)
