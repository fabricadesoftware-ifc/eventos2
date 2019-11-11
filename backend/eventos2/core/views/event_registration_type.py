from django.db import models
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from eventos2.core.models import EventRegistration, EventRegistrationType
from eventos2.core.serializers import (
    EventRegistrationDetailSerializer,
    EventRegistrationTypeCreateSerializer,
    EventRegistrationTypeDetailSerializer,
    EventRegistrationTypeUpdateSerializer,
)


class EventRegistrationTypeViewSet(GenericViewSet):
    queryset = EventRegistrationType.objects.all()

    @swagger_auto_schema(
        request_body=EventRegistrationTypeCreateSerializer,
        responses={200: EventRegistrationTypeDetailSerializer, 400: "Validation error"},
    )
    def create(self, request):
        request_serializer = EventRegistrationTypeCreateSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        registration_type = request_serializer.save()

        response_serializer = EventRegistrationTypeDetailSerializer(registration_type)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=EventRegistrationTypeUpdateSerializer,
        responses={
            200: EventRegistrationTypeDetailSerializer,
            400: "Validation error",
            404: "Not found",
        },
    )
    def update(self, request, *args, **kwargs):
        registration_type = self.get_object()
        request_serializer = EventRegistrationTypeUpdateSerializer(
            registration_type, data=request.data
        )
        request_serializer.is_valid(raise_exception=True)
        registration_type = request_serializer.save()

        response_serializer = EventRegistrationTypeDetailSerializer(registration_type)
        return Response(response_serializer.data)

    @swagger_auto_schema(
        responses={204: "Success", 409: "Unable to delete", 404: "Not found"}
    )
    def destroy(self, request, *args, **kwargs):
        registration_type = self.get_object()
        try:
            registration_type.delete()
        except models.ProtectedError:
            return Response(status=status.HTTP_409_CONFLICT)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={200: EventRegistrationDetailSerializer(many=True)})
    @action(detail=True, url_path="registrations")
    def list_registrations(self, request, *args, **kwargs):
        registration_type = self.get_object()
        registrations = EventRegistration.objects.filter(
            registration_type=registration_type
        )
        serializer = EventRegistrationDetailSerializer(registrations, many=True)
        return Response(serializer.data)
