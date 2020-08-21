from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from eventos2.core.router import router as core_router
from eventos2.media.router import router as media_router

# Junção das rotas de todos os aplicativos
global_router = SimpleRouter()
global_router.registry.extend(core_router.registry)
global_router.registry.extend(media_router.registry)

urlpatterns = [
    path(
        "api/v1/",
        include(
            [
                re_path(r"^schema/$", SpectacularAPIView.as_view(), name="schema"),
                re_path(
                    r"^swagger/$",
                    SpectacularSwaggerView.as_view(url_name="schema"),
                    name="schema-swagger-ui",
                ),
                # Simple health check, used during deployment
                path("health_check", lambda request: HttpResponse("ok")),
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
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
