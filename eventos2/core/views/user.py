from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from eventos2.core.models import Submission, User
from eventos2.core.serializers import (
    ReviewRequestInlineSerializer,
    SubmissionDetailWithReviewsSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from eventos2.utils.permissions import PerActionPermissions
from eventos2.utils.viewsets import CViewSet


class UserViewSet(CViewSet):
    queryset = User.objects.filter(is_active=True)
    permission_classes = [PerActionPermissions]
    per_action_permissions = {
        "list": PerActionPermissions.ALLOW_AUTHENTICATED,
        "create": PerActionPermissions.ALLOW_ANY,
        "current": PerActionPermissions.ALLOW_AUTHENTICATED,
        "current_update": PerActionPermissions.ALLOW_AUTHENTICATED,
        "current_destroy": PerActionPermissions.ALLOW_AUTHENTICATED,
        "current_list_submissions": PerActionPermissions.ALLOW_AUTHENTICATED,
        "current_list_review_requests": PerActionPermissions.ALLOW_AUTHENTICATED,
    }

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    @extend_schema(
        responses={200: UserSerializer(many=True)},
        parameters=[OpenApiParameter("email", required=True)],
    )
    def list(self, request):
        email = request.query_params.get("email")
        users = User.objects.filter(is_active=True, email__iexact=email)
        return Response(self.get_serializer(users, many=True).data)

    @action(
        detail=False,
        url_path="current",
    )
    def current(self, request):
        user = User.objects.filter(is_active=True).get(pk=request.user.pk)
        return Response(self.get_serializer(user).data)

    @current.mapping.put
    def current_update(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = User.objects.filter().get(pk=request.user.pk)

        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.save()

        return Response(serializer.data)

    @current.mapping.delete
    def current_destroy(self, request):
        user = User.objects.filter().get(pk=request.user.pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        responses={200: SubmissionDetailWithReviewsSerializer(many=True)},
    )
    @action(
        detail=False,
        url_path="current/submissions",
        url_name="current-list-submissions",
    )
    def current_list_submissions(self, request, slug=None):
        user = User.objects.filter().get(pk=request.user.pk)

        serializer = SubmissionDetailWithReviewsSerializer(
            Submission.available_objects.filter(authors__in=[user]).order_by("-id"),
            many=True,
        )
        return Response(serializer.data)

    @extend_schema(
        responses={200: ReviewRequestInlineSerializer(many=True)},
    )
    @action(
        detail=False,
        url_path="current/review_requests",
        url_name="current-list-review-requests",
    )
    def current_list_review_requests(self, request, slug=None):
        user = User.objects.filter().get(pk=request.user.pk)

        reviews = user.reviews.order_by("-id").all()
        pending_reviews = [x for x in reviews if x.is_pending]

        serializer = ReviewRequestInlineSerializer(
            pending_reviews,
            many=True,
        )
        return Response(serializer.data)
