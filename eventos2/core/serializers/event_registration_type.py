from rest_framework import serializers

from eventos2.core.models import Event


class EventRegistrationTypeBaseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    name_english = serializers.CharField(
        max_length=255, allow_blank=True, required=False
    )


class EventRegistrationTypeCreateSerializer(EventRegistrationTypeBaseSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.available_objects.all())


class EventRegistrationTypeUpdateSerializer(EventRegistrationTypeBaseSerializer):
    pass


class EventRegistrationTypeDetailSerializer(EventRegistrationTypeBaseSerializer):
    id = serializers.IntegerField()
    event_id = serializers.IntegerField(source="event.id")
