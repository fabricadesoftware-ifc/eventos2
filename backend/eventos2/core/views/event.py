from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from eventos2.core.models import Event, EventRegistration
from eventos2.core.serializers import (
    EventCreateSerializer,
    EventDetailSerializer,
    EventRegistrationDetailSerializer,
    EventUpdateSerializer,
)
from eventos2.utils.permissions import PerActionPermissions


class EventViewSet(GenericViewSet):
    queryset = Event.available_objects.all()
    permission_classes = [PerActionPermissions]
    per_action_permissions = {
        "create": ["core.add_event"],
        "destroy": ["core.delete_event"],
        "list_registrations": ["core.view_event_registration"],
        "retrieve": PerActionPermissions.ALLOW_ANY,
        "update": ["core.change_event"],
    }

    @swagger_auto_schema(
        request_body=EventCreateSerializer,
        responses={201: EventDetailSerializer, 400: "Validation error"},
    )
    def create(self, request):
        request_serializer = EventCreateSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        event = request_serializer.save()

        response_serializer = EventDetailSerializer(event)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: EventDetailSerializer, 404: "Not found"})
    def retrieve(self, request, pk):
        event = event_service.get_by_id(pk)
        return Response(EventDetailSerializer(event).data)

    @swagger_auto_schema(
        request_body=EventUpdateSerializer,
        responses={
            200: EventDetailSerializer,
            400: "Validation error",
            404: "Not found",
        },
    )
    def update(self, request, *args, **kwargs):
        event = self.get_object()
        request_serializer = EventUpdateSerializer(event, data=request.data)
        request_serializer.is_valid(raise_exception=True)
        event = request_serializer.save()

        response_serializer = EventDetailSerializer(event)
        return Response(response_serializer.data)

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={200: EventRegistrationDetailSerializer(many=True)})
    @action(detail=True, url_path="registrations")
    def list_registrations(self, request, pk):
        registrations = event_service.find_registrations(
            actor=request.user, event_id=pk
        )
        out_serializer = EventRegistrationDetailSerializer(registrations, many=True)
        return Response(out_serializer.data)
