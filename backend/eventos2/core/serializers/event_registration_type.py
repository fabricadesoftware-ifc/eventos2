from rest_framework import serializers

from eventos2.core.models import EventRegistrationType


class EventRegistrationTypeBaseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    name_english = serializers.CharField(
        max_length=255, allow_blank=True, required=False
    )


class EventRegistrationTypeCreateSerializer(EventRegistrationTypeBaseSerializer):
    def create(self, validated_data):
        return EventRegistrationType.objects.create(**validated_data)


class EventRegistrationTypeUpdateSerializer(EventRegistrationTypeBaseSerializer):
    def update(self, registration_type, validated_data):
        for k, v in validated_data.items():
            setattr(registration_type, k, v)
        registration_type.save()
        return registration_type


class EventRegistrationTypeDetailSerializer(EventRegistrationTypeBaseSerializer):
    id = serializers.IntegerField()
