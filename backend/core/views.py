from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Event, Sponsorship, SponsorshipCategory, User
from core.serializers import (
    EventSerializer,
    SponsorshipCategorySerializer,
    SponsorshipDetailSerializer,
    UserCreateSerializer,
    UserSerializer,
)


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action == "create":
            permission_classes = []
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    @action(detail=False, url_path="current")
    def current(self, request):
        instance = self.queryset.get(pk=self.request.user.pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @current.mapping.put
    def current_update(self, request):
        instance = self.queryset.get(pk=self.request.user.pk)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @current.mapping.delete
    def current_destroy(self, request):
        instance = self.queryset.get(pk=self.request.user.pk)
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.available_objects.all()
    serializer_class = EventSerializer


class SponsorshipViewSet(viewsets.ModelViewSet):
    queryset = Sponsorship.objects.all()
    serializer_class = SponsorshipDetailSerializer


class SponsorshipCategoryViewSet(viewsets.ModelViewSet):
    queryset = SponsorshipCategory.objects.all()
    serializer_class = SponsorshipCategorySerializer
