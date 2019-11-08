from rest_framework import serializers

from eventos2.core.models import EventRegistration, EventRegistrationType, User
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

    def validate(self, data):
        event = data["registration_type"].event
        registrations_for_user = data["user"].event_registrations.filter(event=event)
        if registrations_for_user.exists():
            raise serializers.ValidationError(
                "O usuário já está inscrito neste evento."
            )
        return data

    def create(self, validated_data):
        return EventRegistration.objects.create(**validated_data)


class EventRegistrationDetailSerializer(EventRegistrationBaseSerializer):
    id = serializers.IntegerField()
    registration_type = EventRegistrationTypeDetailSerializer()
    user = UserDetailSerializer()
