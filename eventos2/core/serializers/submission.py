from rest_framework import serializers

from eventos2.core.models import Track, User
from eventos2.core.serializers.submission_document import SubmissionDocumentSerializer
from eventos2.core.serializers.track import TrackSerializer
from eventos2.core.serializers.user import UserSerializer


class SubmissionBaseSerializer(serializers.Serializer):
    pass


class SubmissionCreateSerializer(SubmissionBaseSerializer):
    track = serializers.SlugRelatedField(
        slug_field="slug", queryset=Track.objects.all()
    )
    title = serializers.CharField(
        help_text="The submission's title in its native language", max_length=255
    )
    title_english = serializers.CharField(
        allow_blank=True,
        help_text="The submission's name in english",
        max_length=255,
        required=False,
    )
    other_authors = serializers.SlugRelatedField(
        slug_field="public_id",
        queryset=User.objects.filter(is_active=True),
        many=True,
        required=False,
    )

    def validate(self, data):
        if not data["track"].is_open:
            raise serializers.ValidationError(
                {"track": "Submissions to this track are closed."}
            )
        return data


class SubmissionDetailSerializer(SubmissionBaseSerializer):
    id = serializers.IntegerField()
    track = TrackSerializer()
    title = serializers.CharField()
    title_english = serializers.CharField(required=False)
    authors = UserSerializer(many=True)
    documents = SubmissionDocumentSerializer(many=True)
