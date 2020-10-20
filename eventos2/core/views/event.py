from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response

from eventos2.core.models import Event, Submission
from eventos2.core.serializers import (
    ActivitySerializer,
    EventRegistrationDetailSerializer,
    EventSerializer,
    SubmissionDetailWithReviewsSerializer,
    TrackSerializer,
)
from eventos2.utils.permissions import PerActionPermissions
from eventos2.utils.viewsets import CRUDViewSet


class EventViewSet(CRUDViewSet):
    lookup_field = "slug"
    queryset = Event.available_objects.all()
    filter_backends = [filters.SearchFilter]
    serializer_class = EventSerializer
    permission_classes = [PerActionPermissions]
    per_action_permissions = {
        "create": "core.add_event",
        "retrieve": PerActionPermissions.ALLOW_ANY,
        "update": "core.change_event",
        "destroy": "core.delete_event",
        "list_registrations": "core.view_registrations_for_event",
        "list_activities": "core.view_activities_for_event",
        "list_tracks": "core.view_tracks_for_event",
        "list_submissions": "core.view_submissions_for_event",
    }

    @extend_schema(responses={200: EventRegistrationDetailSerializer(many=True)})
    @action(detail=True, url_path="registrations", url_name="list-registrations")
    def list_registrations(self, request, slug=None):
        event = self.get_object()
        serializer = EventRegistrationDetailSerializer(event.registrations, many=True)
        return Response(serializer.data)

    @extend_schema(responses={200: ActivitySerializer(many=True)})
    @action(detail=True, url_path="activities", url_name="list-activities")
    def list_activities(self, request, slug=None):
        event = self.get_object()
        serializer = ActivitySerializer(
            event.activities(manager="available_objects"), many=True
        )
        return Response(serializer.data)

    @extend_schema(responses={200: TrackSerializer(many=True)})
    @action(detail=True, url_path="tracks", url_name="list-tracks")
    def list_tracks(self, request, slug=None):
        event = self.get_object()
        serializer = TrackSerializer(
            event.tracks(manager="available_objects"), many=True
        )
        return Response(serializer.data)

    @extend_schema(
        responses={200: SubmissionDetailWithReviewsSerializer(many=True)},
        parameters=[OpenApiParameter("track", type=int), OpenApiParameter("title")],
    )
    @action(detail=True, url_path="submissions", url_name="list-submissions")
    def list_submissions(self, request, slug=None):
        event = self.get_object()

        track_id = request.query_params.get("track")
        title = request.query_params.get("title")

        filters = {"track__event": event}

        if track_id:
            filters["track__pk"] = track_id
        if title:
            filters["title__unaccent__icontains"] = title

        serializer = SubmissionDetailWithReviewsSerializer(
            Submission.available_objects.filter(**filters).order_by("title"), many=True
        )
        return Response(serializer.data)
