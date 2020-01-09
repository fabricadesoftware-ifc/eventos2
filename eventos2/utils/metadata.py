from rest_framework.metadata import BaseMetadata


# Usado para que viewsets sem queryset não gerem erros
# em requests OPTIONS.
class MinimalMetadata(BaseMetadata):
    """
    Don't include field and other information for `OPTIONS` requests.
    Just return the name and description.
    """

    def determine_metadata(self, request, view):
        return {
            "name": view.get_view_name(),
            "description": view.get_view_description(),
        }
