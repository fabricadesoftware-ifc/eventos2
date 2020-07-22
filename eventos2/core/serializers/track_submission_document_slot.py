from rest_framework import serializers

from eventos2.core.models import Track, TrackSubmissionDocumentSlot


class TrackSubmissionDocumentSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackSubmissionDocumentSlot
        fields = ["id", "name", "name_english", "starts_on", "ends_on"]

    def create(self, validated_data):  # pragma: no cover - no complexity
        raise NotImplementedError("Use TrackSubmissionDocumentSlotCreateSerializer")


class TrackSubmissionDocumentSlotCreateSerializer(serializers.ModelSerializer):
    track_slug = serializers.SlugRelatedField(
        source="track",
        slug_field="slug",
        queryset=Track.available_objects.all(),
        write_only=True,
    )

    class Meta:
        model = TrackSubmissionDocumentSlot
        fields = ["track_slug", "id", "name", "name_english", "starts_on", "ends_on"]
