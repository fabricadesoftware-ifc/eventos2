from rest_framework import mixins, status, viewsets
from rest_framework.response import Response


class CreateModelMixin:
    """
    Same as DRF CreateModelMixin, but returns 200 OK instead of 201 Created.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateModelMixin(object):
    """
    Same as DRF UpdateModelMixin, but doesn't enable partial updates (PATCH).
    """

    def update(self, request, *args, **kwargs):
        return mixins.UpdateModelMixin.update(self, request, *args, **kwargs)

    def perform_update(self, serializer):
        return mixins.UpdateModelMixin.perform_update(self, serializer)


class CViewSet(
    CreateModelMixin, viewsets.GenericViewSet,
):
    """
    Create only.
    """


class CUDViewSet(
    CreateModelMixin,
    UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Create, update, and delete.
    """


class CRUDViewSet(
    CreateModelMixin,
    mixins.RetrieveModelMixin,
    UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Create, retrieve, update, and delete.
    """
