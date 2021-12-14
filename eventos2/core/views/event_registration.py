from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from eventos2.core.models import Event, EventRegistration, User
from eventos2.core.serializers import (
    EventRegistrationBaseSerializer,
    EventRegistrationCreateSerializer,
    EventRegistrationDetailSerializer,
)


class EventRegistrationViewSet(GenericViewSet):
    queryset = EventRegistration.objects.all()

    def get_serializer_class(self):
        return {
            "create": EventRegistrationCreateSerializer,
            "destroy": EventRegistrationBaseSerializer,
            "list": EventRegistrationBaseSerializer,
        }.get(self.action, None)

    @extend_schema(
        responses={200: EventRegistrationDetailSerializer},
    )
    def create(self, request):
        in_serializer = self.get_serializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data

        event = data["event"]

        if not request.user.has_perm("core.register_self_into_event"):
            raise PermissionDenied(
                "You're not authorized to self register into this event."
            )

        if self.get_queryset().filter(event=event, user=request.user).exists():
            raise ValidationError("This registration already exists.")

        event_registration = EventRegistration.objects.create(
            event=event, user=request.user
        )

        out_serializer = EventRegistrationDetailSerializer(event_registration)
        return Response(out_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        registration = self.get_object()

        is_self_unregistering = request.user == registration.user
        if not is_self_unregistering:
            raise PermissionDenied("You're not authorized remove this registration.")

        registration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        responses={200: EventRegistrationDetailSerializer(many=True)},
        parameters=[
            OpenApiParameter("user_public_id", required=True),
            OpenApiParameter("event_slug"),
        ],
    )
    def list(self, request):
        user_public_id = request.query_params.get("user_public_id")
        event_slug = request.query_params.get("event_slug")

        user = User.objects.filter(public_id=user_public_id).first()
        event = Event.available_objects.filter(slug=event_slug).first()

        if request.user != user:
            raise PermissionDenied(
                "You're not authorized to view registrations for this user."
            )

        if event_slug is not None:
            registrations = self.get_queryset().filter(event=event, user=user)
        else:
            registrations = self.get_queryset().filter(user=user)

        out_serializer = EventRegistrationDetailSerializer(registrations, many=True)
        return Response(out_serializer.data)
