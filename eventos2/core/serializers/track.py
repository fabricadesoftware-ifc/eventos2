from rest_framework import serializers

from eventos2.core.models.event import Event


class TrackBaseSerializer(serializers.Serializer):
    slug = serializers.CharField(
        help_text="A unique, readable identifier", max_length=255
    )
    name = serializers.CharField(
        help_text="The track's name in its native language", max_length=255
    )
    name_english = serializers.CharField(
        allow_blank=True,
        help_text="The track's name in english",
        max_length=255,
        required=False,
    )


class TrackCreateSerializer(TrackBaseSerializer):
    event = serializers.SlugRelatedField(
        slug_field="slug", queryset=Event.objects.all()
    )


class TrackUpdateSerializer(TrackBaseSerializer):
    pass


class TrackDetailSerializer(TrackBaseSerializer):
    pass
