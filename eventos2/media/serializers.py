from rest_framework import serializers

from eventos2.media.models import Document, Image
from eventos2.utils.files import (
    CONTENT_TYPE_DOC,
    CONTENT_TYPE_DOCX,
    CONTENT_TYPE_JPG,
    CONTENT_TYPE_ODT,
    CONTENT_TYPE_PDF,
    CONTENT_TYPE_PNG,
    CONTENT_TYPE_TEX,
    get_content_type,
)


class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["attachment_key", "content_type", "file", "uploaded_on"]
        read_only_fields = ["attachment_key", "content_type", "uploaded_on"]
        extra_kwargs = {"file": {"write_only": True}}

    def validate(self, data):
        content_type = get_content_type(data["file"])

        valid_content_types = [
            CONTENT_TYPE_DOC,
            CONTENT_TYPE_DOCX,
            CONTENT_TYPE_ODT,
            CONTENT_TYPE_PDF,
            CONTENT_TYPE_TEX,
        ]
        if content_type not in valid_content_types:
            raise serializers.ValidationError(
                {"file": "Invalid or corrupted document."}
            )

        # save the serializer to the model
        # # so we don't need to read the file to get it every time
        data["content_type"] = content_type
        return data


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["url", "uploaded_on", "content_type"]
        read_only_fields = ["url", "uploaded_on", "content_type"]

    def create(self, validated_data):  # pragma: no cover - only disabling creation
        raise NotImplementedError("Use DocumentUploadSerializer to create files.")


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["attachment_key", "file", "description", "uploaded_on"]
        read_only_fields = ["attachment_key", "uploaded_on"]
        extra_kwargs = {"file": {"write_only": True}}

    def validate_file(self, value):
        valid_content_types = [CONTENT_TYPE_JPG, CONTENT_TYPE_PNG]
        if value.content_type not in valid_content_types:
            raise serializers.ValidationError("Invalid or corrupted image.")
        return value


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["url", "description", "uploaded_on"]
        read_only_fields = ["url", "description", "uploaded_on"]

    def create(self, validated_data):  # pragma: no cover - only disabling creation
        raise NotImplementedError("Use ImageUploadSerializer to create images.")
