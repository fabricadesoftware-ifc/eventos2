from drf_yasg.openapi import IN_QUERY, TYPE_INTEGER, Parameter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from eventos2.core.serializers import (
    EventRegistrationCreateSerializer,
    EventRegistrationDetailSerializer,
)
from eventos2.core.services import event as event_service
from eventos2.core.services import event_registration as event_registration_service
from eventos2.core.services import user as user_service
from eventos2.utils.exceptions import NotFoundError


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

        try:
            user = user_service.get_by_id(user_id)
        except NotFoundError:
            user = None

        try:
            event = event_service.get_by_id(event_id)
        except NotFoundError:
            event = None

        if event_id is not None:
            registrations = event_registration_service.find_by_user_and_event(
                actor=request.user, user=user, event=event
            )
        else:
            registrations = event_registration_service.find_by_user(
                actor=request.user, user=user
            )

        out_serializer = EventRegistrationDetailSerializer(registrations, many=True)
        return Response(out_serializer.data)
