from rest_framework import serializers

from eventos2.core.models import Track, User
from eventos2.core.serializers.track import TrackDetailSerializer
from eventos2.core.serializers.user import UserDetailSerializer


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


class SubmissionDetailSerializer(SubmissionBaseSerializer):
    id = serializers.IntegerField()
    track = TrackDetailSerializer()
    title = serializers.CharField()
    title_english = serializers.CharField(required=False)
    authors = UserDetailSerializer(many=True)
