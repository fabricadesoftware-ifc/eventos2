from rest_framework import serializers

from eventos2.core.models.event import Event


class ActivityBaseSerializer(serializers.Serializer):
    slug = serializers.CharField(
        help_text="A unique, readable identifier", max_length=255
    )
    name = serializers.CharField(
        help_text="The activity's name in its native language", max_length=255
    )
    name_english = serializers.CharField(
        allow_blank=True,
        help_text="The activity's name in english",
        max_length=255,
        required=False,
    )
    starts_on = serializers.DateTimeField()
    ends_on = serializers.DateTimeField()


class ActivityCreateSerializer(ActivityBaseSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())


class ActivityUpdateSerializer(ActivityBaseSerializer):
    pass


class ActivityDetailSerializer(ActivityBaseSerializer):
    id = serializers.IntegerField()
