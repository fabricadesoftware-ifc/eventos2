from rest_framework import serializers

from eventos2.core.models import SubmissionDocument
from eventos2.media.models import Document
from eventos2.media.serializers import DocumentSerializer


class SubmissionDocumentBaseSerializer(serializers.Serializer):
    def validate(self, data):
        if not data["slot"].is_open:
            raise serializers.ValidationError(
                {"slot": "Submissions to this slot are closed."}
            )
        return data


class SubmissionDocumentSerializer(
    SubmissionDocumentBaseSerializer, serializers.ModelSerializer
):
    document_attachment_key = serializers.SlugRelatedField(
        source="document",
        queryset=Document.objects.all(),
        slug_field="attachment_key",
        required=True,
        write_only=True,
    )
    document = DocumentSerializer(read_only=True)

    class Meta:
        model = SubmissionDocument
        fields = [
            "slot",
            "submission",
            "document",
            "document_attachment_key",
            "submitted_on",
        ]
        extra_kwargs = {
            "submission": {"write_only": True},
            "submitted_on": {"read_only": True},
        }

    def update(self, instance, validated_data):  # pragma: no cover - no complexity
        raise NotImplementedError
