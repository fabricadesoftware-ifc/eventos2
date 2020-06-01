from django.shortcuts import get_object_or_404
from drf_yasg.openapi import IN_QUERY, TYPE_INTEGER, TYPE_STRING, Parameter
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

        if not request.user.has_perm("core.register_self_into_event"):
            raise PermissionDenied(
                "You're not authorized to self register into this event."
            )

        if EventRegistration.objects.filter(event=event, user=request.user).exists():
            raise ValidationError("This registration already exists.")

        event_registration = EventRegistration.objects.create(
            event=event, user=request.user
        )

        out_serializer = EventRegistrationDetailSerializer(event_registration)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def destroy(self, request, pk):
        registration = get_object_or_404(EventRegistration, pk=pk)

        is_self_unregistering = request.user == registration.user
        if not is_self_unregistering:
            raise PermissionDenied("You're not authorized remove this registration.")

        registration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        responses={200: "Success"},
        manual_parameters=[
            Parameter("user_id", in_=IN_QUERY, type=TYPE_INTEGER, required=True),
            Parameter(
                "event_slug",
                in_=IN_QUERY,
                type=TYPE_STRING,
                required=False,
                default=None,
            ),
        ],
    )
    def list(self, request):
        user_id = request.query_params.get("user_id")
        event_slug = request.query_params.get("event_slug")

        user = User.objects.filter(pk=user_id).first()
        event = Event.available_objects.filter(slug=event_slug).first()

        if event_slug is not None:
            registrations = EventRegistration.objects.filter(event=event, user=user)
        else:
            registrations = EventRegistration.objects.filter(user=user)

        out_serializer = EventRegistrationDetailSerializer(registrations, many=True)
        return Response(out_serializer.data)
