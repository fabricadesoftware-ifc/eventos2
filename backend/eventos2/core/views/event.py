from django.db import models
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from eventos2.core.models import Event, EventRegistrationType
from eventos2.core.serializers import (
    EventCreateSerializer,
    EventDetailSerializer,
    EventRegistrationTypeCreateSerializer,
    EventRegistrationTypeDetailSerializer,
    EventRegistrationTypeUpdateSerializer,
    EventUpdateSerializer,
)


class EventViewSet(GenericViewSet):
    queryset = Event.available_objects.all()

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
    def retrieve(self, request, *args, **kwargs):
        event = self.get_object()
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

    @action(detail=True, methods=["post"], url_path="registration_types")
    @swagger_auto_schema(
        request_body=EventRegistrationTypeCreateSerializer,
        responses={
            200: EventRegistrationTypeDetailSerializer,
            400: "Validation error",
            404: "Not found",
        },
    )
    def add_registration_type(self, request, *args, **kwargs):
        event = self.get_object()
        request_serializer = EventRegistrationTypeCreateSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        registration_type = request_serializer.save(event=event)

        response_serializer = EventRegistrationTypeDetailSerializer(registration_type)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["put"],
        url_path=r"registration_types/(?P<registration_type_id>[^/.]+)",
    )
    @swagger_auto_schema(
        request_body=EventRegistrationTypeUpdateSerializer,
        responses={
            200: EventRegistrationTypeDetailSerializer,
            400: "Validation error",
            404: "Not found",
        },
    )
    def update_registration_type(self, request, *args, **kwargs):
        event = self.get_object()
        registration_type = get_object_or_404(
            EventRegistrationType, pk=kwargs["registration_type_id"], event=event
        )
        request_serializer = EventRegistrationTypeUpdateSerializer(
            instance=registration_type, data=request.data
        )
        request_serializer.is_valid(raise_exception=True)
        registration_type = request_serializer.save(event=event)

        response_serializer = EventRegistrationTypeDetailSerializer(registration_type)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @update_registration_type.mapping.delete
    @swagger_auto_schema(responses={204: "Success", 404: "Not found", 409: "Conflict"})
    def detroy_registration_type(self, request, *args, **kwargs):
        event = self.get_object()
        registration_type = get_object_or_404(
            EventRegistrationType, pk=kwargs["registration_type_id"], event=event
        )
        try:
            registration_type.delete()
        except models.ProtectedError:
            return Response(
                data={
                    "detail": (
                        "Esse tipo de inscrição já tem inscrições realizadas."
                        " Não é possível removê-lo."
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
