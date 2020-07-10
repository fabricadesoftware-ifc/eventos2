from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from eventos2.core.models import Submission
from eventos2.core.serializers import (
    SubmissionCreateSerializer,
    SubmissionDetailSerializer,
)


class SubmissionViewSet(ViewSet):
    @swagger_auto_schema(
        request_body=SubmissionCreateSerializer,
        responses={200: SubmissionDetailSerializer, 400: "Validation error"},
    )
    def create(self, request):
        in_serializer = SubmissionCreateSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data

        track = data["track"]

        if not request.user.has_perm("core.add_submission_to_track", track):
            raise PermissionDenied("You're not authorized to submit to this track.")

        submission = Submission.objects.create(
            track=track,
            title=data["title"],
            title_english=data.get("title_english", ""),
        )
        submission.authors.add(request.user)
        submission.authors.add(*data.get("other_authors", []))

        out_serializer = SubmissionDetailSerializer(submission)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)
