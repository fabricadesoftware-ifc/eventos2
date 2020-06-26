from rest_framework import serializers

from eventos2.media.models import Image


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["attachment_key", "file", "description", "uploaded_on"]
        read_only_fields = ["attachment_key", "uploaded_on"]
        extra_kwargs = {"file": {"write_only": True}}

    def validate_file(self, value):
        valid_content_types = ["image/jpeg", "image/png"]
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
