from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from eventos2.core.models import Activity
from eventos2.core.serializers import (
    ActivityCreateSerializer,
    ActivityDetailSerializer,
    ActivityUpdateSerializer,
)


class ActivityViewSet(ViewSet):
    lookup_url_kwarg = "slug"

    @swagger_auto_schema(
        request_body=ActivityCreateSerializer,
        responses={201: ActivityDetailSerializer, 400: "Validation error"},
    )
    def create(self, request):
        in_serializer = ActivityCreateSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data
        event = data["event"]

        if not request.user.has_perm("core.change_event", event):
            raise PermissionDenied("Not authorized to add an activity to this event.")

        if Activity.objects.filter(slug=data["slug"]).exists():
            raise ValidationError({"slug": ["Slug already used."]})

        activity = Activity.objects.create(
            event=event,
            slug=data["slug"],
            name=data["name"],
            name_english=data.get("name_english", ""),
            starts_on=data["starts_on"],
            ends_on=data["ends_on"],
        )

        out_serializer = ActivityDetailSerializer(activity)
        return Response(out_serializer.data, status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: ActivityDetailSerializer, 404: "Not found"})
    def retrieve(self, request, slug):
        activity = get_object_or_404(Activity.available_objects, slug=slug)

        if not request.user.has_perm("core.view_activities_for_event", activity.event):
            raise PermissionDenied("Not authorized to view this activity")

        return Response(ActivityDetailSerializer(activity).data)

    @swagger_auto_schema(
        request_body=ActivityUpdateSerializer,
        responses={
            200: ActivityDetailSerializer,
            400: "Validation error",
            404: "Not found",
            409: "Slug already used",
        },
    )
    def update(self, request, slug):
        activity = get_object_or_404(Activity.available_objects, slug=slug)

        in_serializer = ActivityUpdateSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        data = in_serializer.validated_data

        if not request.user.has_perm("core.change_event", activity.event):
            raise PermissionDenied("Not authorized to edit this activity.")

        is_new_slug = activity.slug != data["slug"]
        new_slug_exists = Activity.available_objects.filter(slug=data["slug"]).exists()

        if is_new_slug and new_slug_exists:
            raise ValidationError("Slug already used.")

        activity.slug = data["slug"]
        activity.name = data["name"]
        activity.name_english = data.get("name_english", "")
        activity.starts_on = data["starts_on"]
        activity.ends_on = data["ends_on"]
        activity.save()

        out_serializer = ActivityDetailSerializer(activity)
        return Response(out_serializer.data)

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def destroy(self, request, slug):
        activity = get_object_or_404(Activity.available_objects, slug=slug)

        if not request.user.has_perm("core.change_event", activity.event):
            raise PermissionDenied("Not authorized to delete this activity.")

        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
