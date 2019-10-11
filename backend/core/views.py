from rest_framework import viewsets

from core.models import Event, Sponsorship, SponsorshipCategory
from core.serializers import (
    EventSerializer,
    SponsorshipCategorySerializer,
    SponsorshipDetailSerializer,
)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.available_objects.all()
    serializer_class = EventSerializer


class SponsorshipViewSet(viewsets.ModelViewSet):
    queryset = Sponsorship.objects.all()
    serializer_class = SponsorshipDetailSerializer


class SponsorshipCategoryViewSet(viewsets.ModelViewSet):
    queryset = SponsorshipCategory.objects.all()
    serializer_class = SponsorshipCategorySerializer
