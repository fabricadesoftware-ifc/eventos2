from rest_framework import serializers

from eventos2.core.models import Activity, Event


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ["slug", "name", "name_english", "starts_on", "ends_on"]

    def create(self, validated_data):  # pragma: no cover - no complexity
        raise NotImplementedError("Use ActivityCreateSerializer")


class ActivityCreateSerializer(serializers.ModelSerializer):
    event_slug = serializers.SlugRelatedField(
        source="event", slug_field="slug", queryset=Event.objects.all(), write_only=True
    )

    class Meta:
        model = Activity
        fields = ["event_slug", "slug", "name", "name_english", "starts_on", "ends_on"]
