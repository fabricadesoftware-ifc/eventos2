from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from backend import __version__

schema_view = get_schema_view(
    openapi.Info(title="Eventos2", default_version=__version__),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "api/v1/",
        include(
            [
                path("admin/", admin.site.urls),
                re_path(
                    r"^swagger(?P<format>\.json|\.yaml)$",
                    schema_view.without_ui(cache_timeout=0),
                    name="schema-json",
                ),
                re_path(
                    r"^swagger/$",
                    schema_view.with_ui("swagger", cache_timeout=0),
                    name="schema-swagger-ui",
                ),
                re_path(
                    r"^redoc/$",
                    schema_view.with_ui("redoc", cache_timeout=0),
                    name="schema-redoc",
                ),
                path("", include("core.urls")),
                path("image", include("images.urls")),
            ]
        ),
    )
]

# Servir arquivos de media. Só será efetivo quando rodando no modo debug.
# Em produção, o nginx é quem serve estes arquivos.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
