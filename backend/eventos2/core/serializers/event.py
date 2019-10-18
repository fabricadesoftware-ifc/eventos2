from rest_framework import serializers

from eventos2.core.models import Event, Sponsorship, SponsorshipCategory
from eventos2.images.models import Image
from eventos2.images.serializers import ImageSerializer


class SponsorshipCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorshipCategory
        fields = ["id", "name"]


class SponsorshipSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Sponsorship
        fields = ["sponsor", "category"]


class SponsorshipDetailSerializer(serializers.ModelSerializer):
    category = SponsorshipCategorySerializer()

    class Meta:
        model = Sponsorship
        fields = ["id", "sponsored_event", "sponsor", "category"]


class EventSerializer(serializers.ModelSerializer):
    sponsorships = SponsorshipSerializer(many=True, required=False, read_only=True)
    logo_attachment_key = serializers.SlugRelatedField(
        source="logo",
        queryset=Image.objects.all(),
        slug_field="attachment_key",
        required=False,
        write_only=True,
        error_messages={
            "does_not_exist": "Image with {slug_name}={value} does not exist"
        },
    )
    logo = ImageSerializer(required=False, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "name_english",
            "starts_on",
            "ends_on",
            "sponsorships",
            "logo_attachment_key",
            "logo",
        ]
        read_only_fields = ["sponsorships", "logo"]
