from rest_framework import serializers

from core.models import Event, Image, Sponsorship, SponsorshipCategory


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
    sponsorships = SponsorshipSerializer(many=True)

    class Meta:
        model = Event
        fields = ["id", "name", "name_english", "starts_on", "ends_on", "sponsorships"]
        read_only_fields = ["sponsorships"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["public_id", "file", "description", "uploaded_at"]
        read_only_fields = ["public_id", "uploaded_at"]
        extra_kwargs = {"file": {"write_only": True}}
