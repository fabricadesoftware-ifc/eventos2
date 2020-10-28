from rest_framework import serializers

from eventos2.core.models import Review, ReviewAnswer
from eventos2.core.serializers.review_answer import ReviewAnswerSerializer
from eventos2.core.serializers.submission import SubmissionDetailSerializer
from eventos2.core.serializers.user import UserSerializer


class ReviewCreateSerializer(serializers.Serializer):
    request = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all())
    answers = ReviewAnswerSerializer(many=True)

    def validate(self, data):
        request = data["request"]

        if not request.is_pending:
            raise serializers.ValidationError(
                {"request": "This review has already been completed."}
            )

        track = request.submission.track
        answers = data["answers"]

        # If this wasn't here, the request would succeed
        # but not do anything, and the review would still be pending.
        if len(answers) == 0:  # pragma: no cover
            raise serializers.ValidationError(
                {"answers": "At least one answer must be provided."}
            )

        questions_required = set(track.review_questions.values_list("id", flat=True))
        questions_answered = set(x["question"].id for x in answers)

        if questions_required != questions_answered:
            raise serializers.ValidationError(
                {"answers": "All required questions must be answered."}
            )

        return data

    def create(self, validated_data):
        answers_data = validated_data.pop("answers")

        for answer_data in answers_data:
            ReviewAnswer.objects.create(review=validated_data["request"], **answer_data)

        return validated_data["request"]


class ReviewDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    submission = SubmissionDetailSerializer()
    author = UserSerializer()
    answers = ReviewAnswerSerializer(many=True)
