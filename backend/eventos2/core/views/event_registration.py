from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from eventos2.core.models import EventRegistration
from eventos2.core.serializers import (
    EventRegistrationCreateSerializer,
    EventRegistrationDetailSerializer,
)


class EventRegistrationViewSet(GenericViewSet):
    queryset = EventRegistration.objects.all()

    @swagger_auto_schema(
        request_body=EventRegistrationCreateSerializer,
        responses={200: EventRegistrationDetailSerializer, 400: "Validation error"},
    )
    def create(self, request):
        request_serializer = EventRegistrationCreateSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        event_registration = request_serializer.save()

        response_serializer = EventRegistrationDetailSerializer(event_registration)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def destroy(self, request, *args, **kwargs):
        registration = self.get_object()
        registration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
