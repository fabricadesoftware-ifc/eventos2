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

        review_request = data["request"]
        if not request.user.has_perm("core.answer_review", review_request):
            raise PermissionDenied("You're not authorized to review this submission.")

        review = in_serializer.save(author=request.user)

        out_serializer = ReviewDetailSerializer(review)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)
