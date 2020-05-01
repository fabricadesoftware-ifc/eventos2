from django.shortcuts import get_object_or_404
from drf_yasg.openapi import IN_QUERY, TYPE_INTEGER, Parameter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from eventos2.core.models import Event, EventRegistration, User
from eventos2.core.serializers import (
    EventRegistrationCreateSerializer,
    EventRegistrationDetailSerializer,
)


class EventRegistrationViewSet(ViewSet):
    @swagger_auto_schema(
        request_body=EventRegistrationCreateSerializer,
        responses={
            200: EventRegistrationDetailSerializer,
            400: "Validation error",
            404: "Not found",
        },
    )
    def create(self, request):
        in_serializer = EventRegistrationCreateSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data

        event = data["event"]
        target = data["user"]

        is_self_registering = request.user == target
        cannot_self_register = not request.user.has_perm(
            "core.register_self_into_event", event
        )
        cannot_register_anyone = not request.user.has_perm("core.change_event", event)

        if is_self_registering and cannot_self_register and cannot_register_anyone:
            raise PermissionDenied(
                "You're not authorized to self register into this event."
            )
        elif not is_self_registering and cannot_register_anyone:
            raise PermissionDenied(
                "You're not authorized to register an user into this event."
            )

        if EventRegistration.objects.filter(event=event, user=target).exists():
            raise ValidationError("This registration already exists.")

        event_registration = EventRegistration.objects.create(event=event, user=target)

        out_serializer = EventRegistrationDetailSerializer(event_registration)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def destroy(self, request, pk):
        registration = get_object_or_404(EventRegistration, pk=pk)

        is_self_unregistering = request.user == registration.user
        can_unregister_anyone = request.user.has_perm(
            "core.change_event", registration.event
        )

        if not (is_self_unregistering or can_unregister_anyone):
            raise PermissionDenied("You're not authorized remove this registration.")

        registration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        responses={200: "Success"},
        manual_parameters=[
            Parameter("user_id", in_=IN_QUERY, type=TYPE_INTEGER, required=True),
            Parameter(
                "event_id",
                in_=IN_QUERY,
                type=TYPE_INTEGER,
                required=False,
                default=None,
            ),
        ],
    )
    def list(self, request):
        user_id = request.query_params.get("user_id")
        event_id = request.query_params.get("event_id")

        user = User.objects.filter(pk=user_id).first()
        event = Event.available_objects.filter(pk=event_id).first()

        if event_id is not None:
            registrations = EventRegistration.objects.filter(event=event, user=user)
        else:
            registrations = EventRegistration.objects.filter(user=user)

        out_serializer = EventRegistrationDetailSerializer(registrations, many=True)
        return Response(out_serializer.data)
