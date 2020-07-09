from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from eventos2.core.models import Event, EventRegistration
from eventos2.core.serializers import (
    ActivityDetailSerializer,
    EventCreateSerializer,
    EventDetailSerializer,
    EventRegistrationDetailSerializer,
    EventUpdateSerializer,
    TrackDetailSerializer,
)


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

        if not request.user.has_perm("core.add_event"):
            raise PermissionDenied("Not authorized to create an event.")

        if Event.available_objects.filter(slug=data["slug"]).exists():
            raise ValidationError({"slug": ["Slug already used."]})

        event = Event.objects.create(
            slug=data["slug"],
            name=data["name"],
            name_english=data.get("name_english", ""),
            starts_on=data["starts_on"],
            ends_on=data["ends_on"],
            logo=data.get("logo"),
        )
        event.owners.add(request.user)

        out_serializer = EventDetailSerializer(event)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: EventDetailSerializer, 404: "Not found"})
    def retrieve(self, request, slug):
        event = get_object_or_404(Event.available_objects, slug=slug)
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
        event = get_object_or_404(Event.available_objects, slug=slug)

        in_serializer = EventUpdateSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data

        if not request.user.has_perm("core.change_event", event):
            raise PermissionDenied("Not authorized to edit this event.")

        is_new_slug = event.slug != data["slug"]
        new_slug_exists = Event.available_objects.filter(slug=data["slug"]).exists()

        if is_new_slug and new_slug_exists:
            raise ValidationError({"slug": ["Slug already used."]})

        event.slug = data["slug"]
        event.name = data["name"]
        event.name_english = data.get("name_english", "")
        event.starts_on = data["starts_on"]
        event.ends_on = data["ends_on"]
        event.logo = data.get("logo")
        event.save()

        out_serializer = EventDetailSerializer(event)
        return Response(out_serializer.data)

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def destroy(self, request, slug):
        event = get_object_or_404(Event.available_objects, slug=slug)

        if not request.user.has_perm("core.delete_event", event):
            raise PermissionDenied("Not authorized to delete this event.")

        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={200: EventRegistrationDetailSerializer(many=True)})
    @action(detail=True, url_path="registrations", url_name="list-registrations")
    def list_registrations(self, request, slug):
        event = get_object_or_404(Event.available_objects, slug=slug)

        if not request.user.has_perm("core.view_registrations_for_event", event):
            raise PermissionDenied(
                "Not authorized to view registrations for this event"
            )

        registrations = EventRegistration.objects.filter(event=event)

        out_serializer = EventRegistrationDetailSerializer(registrations, many=True)
        return Response(out_serializer.data)

    @swagger_auto_schema(responses={200: ActivityDetailSerializer(many=True)})
    @action(detail=True, url_path="activities", url_name="list-activities")
    def list_activities(self, request, slug):
        event = get_object_or_404(Event.available_objects, slug=slug)

        if not request.user.has_perm("core.view_activities_for_event", event):
            raise PermissionDenied("Not authorized to view activities for this event")

        out_serializer = ActivityDetailSerializer(event.activities, many=True)
        return Response(out_serializer.data)

    @swagger_auto_schema(responses={200: TrackDetailSerializer(many=True)})
    @action(detail=True, url_path="tracks", url_name="list-tracks")
    def list_tracks(self, request, slug):
        event = get_object_or_404(Event.available_objects, slug=slug)

        if not request.user.has_perm("core.view_tracks_for_event", event):
            raise PermissionDenied("Not authorized to view tracks for this event")

        out_serializer = TrackDetailSerializer(
            event.tracks(manager="available_objects"), many=True
        )
        return Response(out_serializer.data)
