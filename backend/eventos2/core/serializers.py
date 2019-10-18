from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from eventos2.images.models import Image
from eventos2.images.serializers import ImageSerializer

from .models import Event, Sponsorship, SponsorshipCategory, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
        read_only_fields = ["email"]


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)

    def validate_password(self, value):
        if validate_password(value) is not None:
            raise serializers.ValidationError("Invalid password")
        return make_password(value)

    def create(self, validated_data):
        return User.objects.create(**validated_data, username=validated_data["email"])


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
