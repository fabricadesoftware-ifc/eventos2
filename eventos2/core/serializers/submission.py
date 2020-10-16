from django.utils import timezone
from rest_framework import serializers

from eventos2.core.models import (
    Document,
    Submission,
    SubmissionDocument,
    Track,
    TrackSubmissionDocumentSlot,
    User,
)
from eventos2.core.serializers.submission_document import (
    SubmissionDocumentBaseSerializer,
    SubmissionDocumentSerializer,
)
from eventos2.core.serializers.track import TrackSerializer
from eventos2.core.serializers.user import UserSerializer
from eventos2.media.serializers import DocumentSerializer


class SubmissionDocumentInlineSerializer(SubmissionDocumentBaseSerializer):
    slot = serializers.PrimaryKeyRelatedField(
        queryset=TrackSubmissionDocumentSlot.objects.all(), write_only=True
    )
    document_attachment_key = serializers.SlugRelatedField(
        source="document",
        queryset=Document.objects.all(),
        slug_field="attachment_key",
        required=True,
        write_only=True,
    )
    document = DocumentSerializer(read_only=True)


class SubmissionBaseSerializer(serializers.Serializer):
    pass


class SubmissionCreateSerializer(SubmissionBaseSerializer):
    track = serializers.PrimaryKeyRelatedField(queryset=Track.objects.all())
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
    documents = SubmissionDocumentInlineSerializer(many=True, required=False)

    def validate(self, data):
        track = data["track"]

        if not track.is_open:
            raise serializers.ValidationError(
                {"track": "Submissions to this track are closed."}
            )

        slots_submitted = set(x["slot"].id for x in data.get("documents", []))

        now = timezone.now()
        track_slots = track.submission_document_slots.all()
        slots_valid = set(x.id for x in track_slots if x.is_open_on(now))

        slots_missing = slots_valid - slots_submitted
        slots_invalid = slots_submitted - slots_valid

        # The documents provided by the user must match
        # the currently open slots for the track.
        if slots_missing:
            raise serializers.ValidationError(
                {"documents": "All open slots must have a document."}
            )

        # The documents provided by the user must be open in the track.
        if slots_invalid:
            raise serializers.ValidationError(
                {"documents": "All document slots have be on the same track."}
            )

        return data

    def create(self, validated_data):
        documents_data = validated_data.pop("documents", [])
        other_authors_data = validated_data.pop("other_authors", [])

        submission = Submission.objects.create(**validated_data)

        if "author" not in self.context:  # pragma: no cover - internal use
            raise RuntimeError(
                "The submitting user must be set using the serializer context."
            )
        submission.authors.add(self.context["author"], *other_authors_data)

        for document_data in documents_data:
            SubmissionDocument.objects.create(submission=submission, **document_data)

        return submission


class SubmissionDetailSerializer(SubmissionBaseSerializer):
    id = serializers.IntegerField()
    track = TrackSerializer()
    title = serializers.CharField()
    title_english = serializers.CharField(required=False)
    authors = UserSerializer(many=True)
    documents = SubmissionDocumentSerializer(many=True)
