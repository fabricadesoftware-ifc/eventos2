from rest_framework import serializers

from eventos2.core.models import Track, TrackReviewQuestion


class TrackReviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackReviewQuestion
        fields = ["id", "text", "answer_type"]

    def create(self, validated_data):  # pragma: no cover - no complexity
        raise NotImplementedError("Use TrackReviewQuestionCreateSerializer")


class TrackReviewQuestionCreateSerializer(serializers.ModelSerializer):
    track = serializers.PrimaryKeyRelatedField(queryset=Track.available_objects.all())

    class Meta:
        model = TrackReviewQuestion
        fields = ["track", "id", "text", "answer_type"]
