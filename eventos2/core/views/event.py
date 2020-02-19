from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from eventos2.core.serializers import (
    EventCreateSerializer,
    EventDetailSerializer,
    EventRegistrationDetailSerializer,
    EventUpdateSerializer,
)
from eventos2.core.services import event as event_service


class EventViewSet(ViewSet):
    lookup_url_kwarg = "slug"

    @swagger_auto_schema(
        request_body=EventCreateSerializer,
        responses={201: EventDetailSerializer, 400: "Validation error"},
    )
    def create(self, request):
        in_serializer = EventCreateSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data

        event = event_service.create(actor=request.user, **data)

        out_serializer = EventDetailSerializer(event)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: EventDetailSerializer, 404: "Not found"})
    def retrieve(self, request, slug):
        event = event_service.get_by_slug(slug)
        return Response(EventDetailSerializer(event).data)

    @swagger_auto_schema(
        request_body=EventUpdateSerializer,
        responses={
            200: EventDetailSerializer,
            400: "Validation error",
            404: "Not found",
            409: "Slug already used",
        },
    )
    def update(self, request, slug):
        event = event_service.get_by_slug(slug)

        in_serializer = EventUpdateSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data

        event = event_service.update(actor=request.user, event_id=event.id, **data)

        out_serializer = EventDetailSerializer(event)
        return Response(out_serializer.data)

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def destroy(self, request, slug):
        event = event_service.get_by_slug(slug)
        event_service.delete(actor=request.user, event_id=event.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={200: EventRegistrationDetailSerializer(many=True)})
    @action(detail=True, url_path="registrations", url_name="list-registrations")
    def list_registrations(self, request, slug):
        event = event_service.get_by_slug(slug)

        registrations = event_service.find_registrations(
            actor=request.user, event_id=event.id
        )
        out_serializer = EventRegistrationDetailSerializer(registrations, many=True)
        return Response(out_serializer.data)
