from rest_framework import serializers

from eventos2.core.models import Event
from eventos2.core.serializers.event import EventDetailSerializer
from eventos2.core.serializers.user import UserDetailSerializer


class EventRegistrationBaseSerializer(serializers.Serializer):
    pass


class EventRegistrationCreateSerializer(EventRegistrationBaseSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())


class EventRegistrationDetailSerializer(EventRegistrationBaseSerializer):
    id = serializers.IntegerField()
    event = EventDetailSerializer()
    user = UserDetailSerializer()
