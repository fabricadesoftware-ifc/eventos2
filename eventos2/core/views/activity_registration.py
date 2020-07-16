from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from eventos2.core.models import ActivityRegistration, Event, EventRegistration, User
from eventos2.core.serializers import (
    ActivityRegistrationBaseSerializer,
    ActivityRegistrationCreateSerializer,
    ActivityRegistrationDetailSerializer,
)


class ActivityRegistrationViewSet(GenericViewSet):
    queryset = ActivityRegistration.objects.all()

    def get_serializer_class(self):
        return {
            "create": ActivityRegistrationCreateSerializer,
            "destroy": ActivityRegistrationBaseSerializer,
            "list": ActivityRegistrationBaseSerializer,
        }.get(self.action, None)

    @extend_schema(responses={200: ActivityRegistrationDetailSerializer})
    def create(self, request):
        in_serializer = self.get_serializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data

        activity = data["activity"]

        if not request.user.has_perm("core.register_self_into_activity", activity):
            raise PermissionDenied(
                "You're not authorized to self register into this activity."
            )

        event_registration = EventRegistration.objects.get(
            event=activity.event, user=request.user
        )
        if (
            self.get_queryset()
            .filter(activity=activity, event_registration__user=request.user)
            .exists()
        ):
            raise ValidationError("This registration already exists.")

        activity_registration = ActivityRegistration.objects.create(
            activity=activity, event_registration=event_registration
        )

        out_serializer = ActivityRegistrationDetailSerializer(activity_registration)
        return Response(out_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        registration = self.get_object()

        is_self_unregistering = request.user == registration.event_registration.user
        if not is_self_unregistering:
            raise PermissionDenied("You're not authorized remove this registration.")

        registration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        responses={200: ActivityRegistrationDetailSerializer(many=True)},
        parameters=[
            OpenApiParameter("user_public_id", required=True),
            OpenApiParameter("event_slug", required=True),
        ],
    )
    def list(self, request):
        user_public_id = request.query_params.get("user_public_id")
        event_slug = request.query_params.get("event_slug")

        user = get_object_or_404(User, public_id=user_public_id)
        event = get_object_or_404(Event.available_objects, slug=event_slug)

        registrations = self.get_queryset().filter(
            activity__event=event, event_registration__user=user
        )
        out_serializer = ActivityRegistrationDetailSerializer(registrations, many=True)
        return Response(out_serializer.data)
