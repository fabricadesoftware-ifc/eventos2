from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from eventos2.core.serializers import ReviewRequestCreateSerializer


class ReviewRequestViewSet(ViewSet):
    @extend_schema(
        request=ReviewRequestCreateSerializer,
        responses={200: ReviewRequestCreateSerializer},
    )
    def create(self, request):
        in_serializer = ReviewRequestCreateSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data

        submission = data["submission"]

        if not request.user.has_perm("core.change_event", submission):
            raise PermissionDenied(
                "You're not authorized to add a review request to this submission."
            )

        review = in_serializer.save()

        out_serializer = ReviewRequestCreateSerializer(review)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)
