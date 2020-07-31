from rest_framework import serializers

from eventos2.core.models import Event
from eventos2.media.models import Image
from eventos2.media.serializers import ImageSerializer


class EventSerializer(serializers.ModelSerializer):
    logo_attachment_key = serializers.SlugRelatedField(
        source="logo",
        queryset=Image.objects.all(),
        slug_field="attachment_key",
        required=False,
        write_only=True,
    )
    logo = ImageSerializer(required=False, read_only=True)

    def validate(self, data):
        if data["ends_on"] <= data["starts_on"]:
            raise serializers.ValidationError(
                {"ends_on": "The event must end after it starts."}
            )
        return data

    class Meta:
        model = Event
        fields = [
            "slug",
            "name",
            "name_english",
            "starts_on",
            "ends_on",
            "logo",
            "logo_attachment_key",
        ]
