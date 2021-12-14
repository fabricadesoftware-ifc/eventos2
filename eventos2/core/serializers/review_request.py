from rest_framework import serializers, validators

from eventos2.core.models import Review, Submission, User
from eventos2.core.serializers.submission import (
    SubmissionDetailWithoutAuthorsSerializer,
)


class ReviewRequestCreateSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="public_id",
        queryset=User.objects.filter(is_active=True),
    )
    submission = serializers.PrimaryKeyRelatedField(
        queryset=Submission.available_objects.all()
    )

    class Meta:
        model = Review
        fields = ["author", "submission"]
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Review.objects.all(), fields=["author", "submission"]
            )
        ]


class ReviewRequestInlineSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    submission = SubmissionDetailWithoutAuthorsSerializer()
