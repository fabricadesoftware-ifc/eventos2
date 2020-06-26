from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from eventos2 import __version__
from eventos2.core.router import router as core_router
from eventos2.media.router import router as media_router

# Junção das rotas de todos os aplicativos
global_router = SimpleRouter()
global_router.registry.extend(core_router.registry)
global_router.registry.extend(media_router.registry)

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
                path("", include(global_router.urls)),
                path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
                path(
                    "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
                ),
            ]
        ),
    )
]

# Habilitar a interface de administração apenas em modo debug.
if settings.DEBUG:  # pragma: no cover - debugging
    urlpatterns.append(path("api/admin/", admin.site.urls))

# Servir arquivos de media. Só será efetivo quando rodando no modo debug.
# Em produção, o nginx é quem serve estes arquivos.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
