from rest_framework import serializers

from eventos2.images.models import Image


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["attachment_key", "file", "description", "uploaded_on"]
        read_only_fields = ["attachment_key", "uploaded_on"]
        extra_kwargs = {"file": {"write_only": True}}


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["url", "description", "uploaded_on"]
        read_only_fields = ["url", "description", "uploaded_on"]

    def create(self, validated_data):  # pragma: no cover - only disabling creation
        raise NotImplementedError("Use ImageUploadSerializer to create images.")
