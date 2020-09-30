from rest_framework import serializers

from eventos2.core.models import Activity, Event


class ActivityBaseSerializer(serializers.Serializer):
    def validate(self, data):
        if data["ends_on"] <= data["starts_on"]:
            raise serializers.ValidationError(
                {"ends_on": "The activity must end after it starts."}
            )

        # when creating, the event is in the input data
        event = data.get("event")
        if event is None:
            # when updating, the event in the instance data
            event = self.instance.event

        dates_are_within_event = (
            event.starts_on <= data["starts_on"] <= data["ends_on"] <= event.ends_on
        )
        if not dates_are_within_event:
            raise serializers.ValidationError(
                {"ends_on": "The activity dates must be within the event's dates."}
            )
        return data


class ActivitySerializer(ActivityBaseSerializer, serializers.ModelSerializer):
    registration_count = serializers.ReadOnlyField(source="registrations.count")

    class Meta:
        model = Activity
        fields = [
            "id",
            "name",
            "name_english",
            "starts_on",
            "ends_on",
            "is_open",
            "registration_count",
        ]

    def create(self, validated_data):  # pragma: no cover - no complexity
        raise NotImplementedError("Use ActivityCreateSerializer")


class ActivityCreateSerializer(ActivityBaseSerializer, serializers.ModelSerializer):
    event_slug = serializers.SlugRelatedField(
        source="event", slug_field="slug", queryset=Event.objects.all(), write_only=True
    )

    class Meta:
        model = Activity
        fields = [
            "id",
            "event_slug",
            "name",
            "name_english",
            "starts_on",
            "ends_on",
            "is_open",
        ]
