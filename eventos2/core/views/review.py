from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from eventos2.core.serializers import ReviewCreateSerializer, ReviewDetailSerializer


class ReviewViewSet(ViewSet):
    @extend_schema(
        request=ReviewCreateSerializer, responses={200: ReviewDetailSerializer}
    )
    def create(self, request):
        in_serializer = ReviewCreateSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data

        submission = data["submission"]

        if not request.user.has_perm("core.add_review_to_submission", submission):
            raise PermissionDenied("You're not authorized to review this submission.")

        review = in_serializer.save(author=request.user)

        out_serializer = ReviewDetailSerializer(review)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)
