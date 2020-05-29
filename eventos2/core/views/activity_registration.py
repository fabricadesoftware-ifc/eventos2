from django.shortcuts import get_object_or_404
from drf_yasg.openapi import IN_QUERY, TYPE_INTEGER, Parameter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from eventos2.core.models import ActivityRegistration, Event, EventRegistration, User
from eventos2.core.serializers import (
    ActivityRegistrationCreateSerializer,
    ActivityRegistrationDetailSerializer,
)


class ActivityRegistrationViewSet(ViewSet):
    @swagger_auto_schema(
        request_body=ActivityRegistrationCreateSerializer,
        responses={200: ActivityRegistrationDetailSerializer, 400: "Validation error"},
    )
    def create(self, request):
        in_serializer = ActivityRegistrationCreateSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data

        activity = data["activity"]

        if not request.user.has_perm("core.register_self_into_activity"):
            raise PermissionDenied(
                "You're not authorized to self register into this activity."
            )

        event_registration = EventRegistration.objects.filter(
            event=activity.event, user=request.user
        ).first()
        if event_registration is None:
            raise ValidationError(
                "You must register to the event"
                " in order to register to one of its activities."
            )

        if ActivityRegistration.objects.filter(
            activity=activity, event_registration__user=request.user
        ).exists():
            raise ValidationError("This registration already exists.")

        activity_registration = ActivityRegistration.objects.create(
            activity=activity, event_registration=event_registration
        )

        out_serializer = ActivityRegistrationDetailSerializer(activity_registration)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def destroy(self, request, pk):
        registration = get_object_or_404(ActivityRegistration, pk=pk)

        is_self_unregistering = request.user == registration.event_registration.user
        if not is_self_unregistering:
            raise PermissionDenied("You're not authorized remove this registration.")

        registration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        responses={200: "Success", 404: "Not found"},
        manual_parameters=[
            Parameter("user_id", in_=IN_QUERY, type=TYPE_INTEGER, required=True),
            Parameter("event_slug", in_=IN_QUERY, type=TYPE_INTEGER, required=True),
        ],
    )
    def list(self, request):
        user_id = request.query_params.get("user_id")
        event_slug = request.query_params.get("event_slug")

        user = get_object_or_404(User, pk=user_id)
        event = get_object_or_404(Event.available_objects, slug=event_slug)

        registrations = ActivityRegistration.objects.filter(
            activity__event=event, event_registration__user=user
        )
        out_serializer = ActivityRegistrationDetailSerializer(registrations, many=True)
        return Response(out_serializer.data)
