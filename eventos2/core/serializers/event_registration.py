from rest_framework import serializers

from eventos2.core.models import EventRegistrationType, User
from eventos2.core.serializers.event_registration_type import (
    EventRegistrationTypeDetailSerializer,
)
from eventos2.core.serializers.user import UserDetailSerializer


class EventRegistrationBaseSerializer(serializers.Serializer):
    pass


class EventRegistrationCreateSerializer(EventRegistrationBaseSerializer):
    registration_type = serializers.PrimaryKeyRelatedField(
        queryset=EventRegistrationType.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


class EventRegistrationDetailSerializer(EventRegistrationBaseSerializer):
    id = serializers.IntegerField()
    registration_type = EventRegistrationTypeDetailSerializer()
    user = UserDetailSerializer()
