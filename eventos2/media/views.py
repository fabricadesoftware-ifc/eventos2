from rest_framework import mixins, parsers, viewsets

from eventos2.media.models import Image
from eventos2.media.serializers import ImageUploadSerializer


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class ImageUploadViewSet(CreateViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageUploadSerializer
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
