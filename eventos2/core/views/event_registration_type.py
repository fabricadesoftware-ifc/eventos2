from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from eventos2.core.serializers import (
    EventRegistrationDetailSerializer,
    EventRegistrationTypeCreateSerializer,
    EventRegistrationTypeDetailSerializer,
    EventRegistrationTypeUpdateSerializer,
)
from eventos2.core.services import (
    event_registration_type as event_registration_type_service,
)


class EventRegistrationTypeViewSet(ViewSet):
    @swagger_auto_schema(
        request_body=EventRegistrationTypeCreateSerializer,
        responses={200: EventRegistrationTypeDetailSerializer, 400: "Validation error"},
    )
    def create(self, request):
        in_serializer = EventRegistrationTypeCreateSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data

        registration_type = event_registration_type_service.create(
            actor=request.user, **data
        )

        out_serializer = EventRegistrationTypeDetailSerializer(registration_type)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=EventRegistrationTypeUpdateSerializer,
        responses={
            200: EventRegistrationTypeDetailSerializer,
            400: "Validation error",
            404: "Not found",
        },
    )
    def update(self, request, pk):
        in_serializer = EventRegistrationTypeUpdateSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data

        registration_type = event_registration_type_service.update(
            actor=request.user, event_registration_type_id=pk, **data
        )

        out_serializer = EventRegistrationTypeDetailSerializer(registration_type)
        return Response(out_serializer.data)

    @swagger_auto_schema(
        responses={204: "Success", 404: "Not found", 409: "Unable to delete"}
    )
    def destroy(self, request, pk):
        event_registration_type_service.delete(
            actor=request.user, event_registration_type_id=pk
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={200: EventRegistrationDetailSerializer(many=True)})
    @action(detail=True, url_path="registrations", url_name="list-registrations")
    def list_registrations(self, request, pk):
        registrations = event_registration_type_service.find_registrations(
            actor=request.user, event_registration_type_id=pk
        )
        out_serializer = EventRegistrationDetailSerializer(registrations, many=True)
        return Response(out_serializer.data)
