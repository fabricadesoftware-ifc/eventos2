from rest_framework import serializers

from eventos2.core.models import SubmissionDocument
from eventos2.media.models import Document
from eventos2.media.serializers import DocumentSerializer


class SubmissionDocumentSerializer(serializers.ModelSerializer):
    document_attachment_key = serializers.SlugRelatedField(
        source="document",
        queryset=Document.objects.all(),
        slug_field="attachment_key",
        required=False,
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
            "slot": {"write_only": True},
            "submission": {"write_only": True},
            "submitted_on": {"read_only": True},
        }

    def update(self, instance, validated_data):  # pragma: no cover - no complexity
        raise NotImplementedError
