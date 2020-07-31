from rest_framework import serializers

from eventos2.core.models import Track, TrackSubmissionDocumentSlot


class TrackSubmissionDocumentSlotBaseSerializer(serializers.Serializer):
    def validate(self, data):
        if data["ends_on"] <= data["starts_on"]:
            raise serializers.ValidationError(
                {"ends_on": "The slot must end after it starts."}
            )

        # when creating, the event is in the input data
        track = data.get("track")
        if track is None:
            # when updating, the event in the instance data
            track = self.instance.track

        dates_are_within_track = (
            track.starts_on <= data["starts_on"] <= data["ends_on"] <= track.ends_on
        )
        if not dates_are_within_track:
            raise serializers.ValidationError(
                {"ends_on": "The slot dates must be within the track's dates."}
            )
        return data


class TrackSubmissionDocumentSlotSerializer(
    TrackSubmissionDocumentSlotBaseSerializer, serializers.ModelSerializer
):
    class Meta:
        model = TrackSubmissionDocumentSlot
        fields = ["id", "name", "name_english", "starts_on", "ends_on"]

    def create(self, validated_data):  # pragma: no cover - no complexity
        raise NotImplementedError("Use TrackSubmissionDocumentSlotCreateSerializer")


class TrackSubmissionDocumentSlotCreateSerializer(
    TrackSubmissionDocumentSlotBaseSerializer, serializers.ModelSerializer
):
    track_slug = serializers.SlugRelatedField(
        source="track",
        slug_field="slug",
        queryset=Track.available_objects.all(),
        write_only=True,
    )

    class Meta:
        model = TrackSubmissionDocumentSlot
        fields = ["track_slug", "id", "name", "name_english", "starts_on", "ends_on"]
