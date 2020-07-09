from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from eventos2.core.models import Track
from eventos2.core.serializers import (
    TrackCreateSerializer,
    TrackDetailSerializer,
    TrackUpdateSerializer,
)


class TrackViewSet(ViewSet):
    lookup_url_kwarg = "slug"

    @swagger_auto_schema(
        request_body=TrackCreateSerializer,
        responses={201: TrackDetailSerializer, 400: "Validation error"},
    )
    def create(self, request):
        in_serializer = TrackCreateSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data
        event = data["event"]

        if not request.user.has_perm("core.change_event", event):
            raise PermissionDenied("Not authorized to add an track to this event.")

        if Track.objects.filter(slug=data["slug"]).exists():
            raise ValidationError({"slug": ["Slug already used."]})

        track = Track.objects.create(
            event=event,
            slug=data["slug"],
            name=data["name"],
            name_english=data.get("name_english", ""),
        )

        out_serializer = TrackDetailSerializer(track)
        return Response(out_serializer.data, status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: TrackDetailSerializer, 404: "Not found"})
    def retrieve(self, request, slug):
        track = get_object_or_404(Track.available_objects, slug=slug)

        if not request.user.has_perm("core.view_tracks_for_event", track.event):
            raise PermissionDenied("Not authorized to view this track")

        return Response(TrackDetailSerializer(track).data)

    @swagger_auto_schema(
        request_body=TrackUpdateSerializer,
        responses={
            200: TrackDetailSerializer,
            400: "Validation error",
            404: "Not found",
            409: "Slug already used",
        },
    )
    def update(self, request, slug):
        track = get_object_or_404(Track.available_objects, slug=slug)

        in_serializer = TrackUpdateSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data

        if not request.user.has_perm("core.change_event", track.event):
            raise PermissionDenied("Not authorized to edit this track.")

        is_new_slug = track.slug != data["slug"]
        new_slug_exists = Track.available_objects.filter(slug=data["slug"]).exists()

        if is_new_slug and new_slug_exists:
            raise ValidationError({"slug": ["Slug already used."]})

        track.slug = data["slug"]
        track.name = data["name"]
        track.name_english = data.get("name_english", "")
        track.save()

        out_serializer = TrackDetailSerializer(track)
        return Response(out_serializer.data)

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def destroy(self, request, slug):
        track = get_object_or_404(Track.available_objects, slug=slug)

        if not request.user.has_perm("core.change_event", track.event):
            raise PermissionDenied("Not authorized to delete this track.")

        track.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
