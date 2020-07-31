from rest_framework import serializers

from eventos2.core.models import Activity
from eventos2.core.serializers.activity import ActivitySerializer
from eventos2.core.serializers.event_registration import (
    EventRegistrationDetailSerializer,
)
from eventos2.core.serializers.user import UserSerializer


class ActivityRegistrationBaseSerializer(serializers.Serializer):
    pass


class ActivityRegistrationCreateSerializer(ActivityRegistrationBaseSerializer):
    activity = serializers.SlugRelatedField(
        slug_field="slug", queryset=Activity.objects.all()
    )

    def validate(self, data):
        if not data["activity"].is_open:
            raise serializers.ValidationError(
                {"activity_slug": "Registrations to this activity are closed."}
            )
        return data


class ActivityRegistrationDetailSerializer(ActivityRegistrationBaseSerializer):
    id = serializers.IntegerField()
    activity = ActivitySerializer()
    event_registration = EventRegistrationDetailSerializer()


class ActivityRegistrationUserListSerializer(ActivityRegistrationBaseSerializer):
    id = serializers.IntegerField()
    user = UserSerializer(source="event_registration.user")
