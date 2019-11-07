from rest_framework import serializers, validators

from eventos2.core.models import Event
from eventos2.images.models import Image
from eventos2.images.serializers import ImageSerializer


class EventBaseSerializer(serializers.Serializer):
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
    slug = serializers.CharField(
        help_text="A unique, readable identifier",
        max_length=255,
        validators=[
            validators.UniqueValidator(
                queryset=Event.objects.all(), message="Este slug já foi utilizado."
            )
        ],
    )
    logo_attachment_key = serializers.SlugRelatedField(
        source="logo",
        queryset=Image.objects.all(),
        slug_field="attachment_key",
        required=False,
    )

    def create(self, validated_data):
        event = Event.objects.create(**validated_data)
        return event


class EventUpdateSerializer(EventBaseSerializer):
    logo_attachment_key = serializers.SlugRelatedField(
        source="logo",
        queryset=Image.objects.all(),
        slug_field="attachment_key",
        required=False,
    )

    def update(self, event, validated_data):
        for k, v in validated_data.items():
            setattr(event, k, v)
        return event


class EventDetailSerializer(EventBaseSerializer):
    slug = serializers.CharField(help_text="A unique, readable identifier")
    logo = ImageSerializer(required=False)
