from rest_framework import serializers, validators

from eventos2.core.models import Event
from eventos2.images.models import Image
from eventos2.images.serializers import ImageSerializer
from eventos2.core.models import EventRegistrationType


class EventRegistrationTypeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    name_english = serializers.CharField(
        max_length=255, allow_blank=True, required=False
    )

    def create(self, validated_data):
        return EventRegistrationType.objects.create(**validated_data)


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
    registration_types = EventRegistrationTypeSerializer(many=True, required=True)

    def validate_registration_types(self, data):
        if len(data) < 1:
            raise serializers.ValidationError(
                "Pelo menos um tipo de inscrição é requerido."
            )
        return data

    def create(self, validated_data):
        registration_types_data = validated_data.pop("registration_types")
        event = Event.objects.create(**validated_data)
        for registration_type_data in registration_types_data:
            registration_type = EventRegistrationTypeSerializer(
                data=registration_type_data
            )
            registration_type.is_valid(raise_exception=True)
            registration_type.save(event=event)
        return event


class EventUpdateSerializer(EventBaseSerializer):
    logo_attachment_key = serializers.SlugRelatedField(
        source="logo",
        queryset=Image.objects.all(),
        slug_field="attachment_key",
        required=False,
    )
    registration_types = EventRegistrationTypeSerializer(many=True, required=True)

    def validate_registration_types(self, data):
        if len(data) < 1:
            raise serializers.ValidationError(
                "Pelo menos um tipo de inscrição é requerido."
            )
        return data

    def update(self, event, validated_data):
        registration_types_data = validated_data.pop("registration_types")
        for k, v in validated_data.items():
            setattr(event, k, v)

        event.registration_types.all().delete()
        for registration_type_data in registration_types_data:
            registration_type = EventRegistrationTypeSerializer(
                data=registration_type_data
            )
            registration_type.is_valid(raise_exception=True)
            registration_type.save(event=event)
        return event


class EventDetailSerializer(EventBaseSerializer):
    slug = serializers.CharField(help_text="A unique, readable identifier")
    logo = ImageSerializer(required=False)
    registration_types = EventRegistrationTypeSerializer(many=True)
