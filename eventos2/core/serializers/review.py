from rest_framework import serializers

from eventos2.core.models import Review, ReviewAnswer, Submission
from eventos2.core.serializers.review_answer import ReviewAnswerSerializer
from eventos2.core.serializers.submission import SubmissionDetailSerializer
from eventos2.core.serializers.user import UserSerializer


class ReviewCreateSerializer(serializers.Serializer):
    submission = serializers.PrimaryKeyRelatedField(
        queryset=Submission.available_objects.all()
    )
    answers = ReviewAnswerSerializer(many=True)

    def validate(self, data):
        track = data["submission"].track
        questions_required = set(track.review_questions.values_list("id", flat=True))
        questions_answered = set(x["question"].id for x in data["answers"])

        if questions_required != questions_answered:
            raise serializers.ValidationError(
                {"answers": "All required questions must be answered."}
            )

        return data

    def create(self, validated_data):
        answers_data = validated_data.pop("answers")

        review = Review.objects.create(**validated_data)

        for answer_data in answers_data:
            ReviewAnswer.objects.create(review=review, **answer_data)

        return review


class ReviewDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    submission = SubmissionDetailSerializer()
    author = UserSerializer()
    answers = ReviewAnswerSerializer(many=True)
