from rest_framework import mixins, viewsets

from core.models import Event, Image, Sponsorship, SponsorshipCategory
from core.serializers import (
    EventSerializer,
    ImageSerializer,
    SponsorshipCategorySerializer,
    SponsorshipDetailSerializer,
)


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.available_objects.all()
    serializer_class = EventSerializer


class SponsorshipViewSet(viewsets.ModelViewSet):
    queryset = Sponsorship.objects.all()
    serializer_class = SponsorshipDetailSerializer


class SponsorshipCategoryViewSet(viewsets.ModelViewSet):
    queryset = SponsorshipCategory.objects.all()
    serializer_class = SponsorshipCategorySerializer


class ImageUploadViewSet(CreateViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
