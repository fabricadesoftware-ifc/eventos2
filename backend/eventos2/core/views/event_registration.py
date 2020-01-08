from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from eventos2.core.serializers import (
    EventRegistrationCreateSerializer,
    EventRegistrationDetailSerializer,
)
from eventos2.core.services import event_registration as event_registration_service


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

        event_registration = event_registration_service.register(
            actor=request.user, **data
        )

        out_serializer = EventRegistrationDetailSerializer(event_registration)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def destroy(self, request, pk):
        event_registration_service.unregister(
            actor=request.user, event_registration_id=pk
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
