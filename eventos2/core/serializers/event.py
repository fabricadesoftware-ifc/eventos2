from rest_framework import serializers

from eventos2.images.models import Image
from eventos2.images.serializers import ImageSerializer


class EventBaseSerializer(serializers.Serializer):
    slug = serializers.CharField(
        help_text="A unique, readable identifier", max_length=255
    )
    name = serializers.CharField(
        help_text="The event's name in its native language", max_length=255
    )
    name_english = serializers.CharField(
        allow_blank=True,
        help_text="The event's name in english",
        max_length=255,
        required=False,
    )
    starts_on = serializers.DateTimeField()
    ends_on = serializers.DateTimeField()


class EventCreateSerializer(EventBaseSerializer):
    logo_attachment_key = serializers.SlugRelatedField(
        source="logo",
        queryset=Image.objects.all(),
        slug_field="attachment_key",
        required=False,
    )


class EventUpdateSerializer(EventBaseSerializer):
    logo_attachment_key = serializers.SlugRelatedField(
        source="logo",
        queryset=Image.objects.all(),
        slug_field="attachment_key",
        required=False,
    )


class EventDetailSerializer(EventBaseSerializer):
    id = serializers.IntegerField()
    logo = ImageSerializer(required=False)
