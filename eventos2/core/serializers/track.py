from rest_framework import serializers

from eventos2.core.models import Event, Track


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ["slug", "name", "name_english", "starts_on", "ends_on"]

    def create(self, validated_data):  # pragma: no cover - no complexity
        raise NotImplementedError("Use ActivityCreateSerializer")


class TrackCreateSerializer(serializers.ModelSerializer):
    event_slug = serializers.SlugRelatedField(
        source="event", slug_field="slug", queryset=Event.objects.all(), write_only=True
    )

    class Meta:
        model = Track
        fields = ["event_slug", "slug", "name", "name_english", "starts_on", "ends_on"]
