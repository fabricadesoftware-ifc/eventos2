from rest_framework import serializers

from eventos2.core.models import TrackReviewQuestion


class ReviewAnswerSerializer(serializers.Serializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=TrackReviewQuestion.objects.all()
    )
    text = serializers.CharField(max_length=255)
