from rest_framework import serializers

from eventos2.core.models import Event
from eventos2.core.serializers.event import EventSerializer
from eventos2.core.serializers.user import UserSerializer


class EventRegistrationBaseSerializer(serializers.Serializer):
    pass


class EventRegistrationCreateSerializer(EventRegistrationBaseSerializer):
    event_slug = serializers.SlugRelatedField(
        source="event", slug_field="slug", queryset=Event.objects.all()
    )

    def validate(self, data):
        if not data["event"].is_open:
            raise serializers.ValidationError(
                {"event_slug": "Registrations to this event are closed."}
            )
        return data


class EventRegistrationDetailSerializer(EventRegistrationBaseSerializer):
    id = serializers.IntegerField()
    event = EventSerializer()
    user = UserSerializer()
