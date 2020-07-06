from rest_framework.routers import DefaultRouter

from eventos2.media import views

app_name = "media"

router = DefaultRouter()
router.register("documents", views.DocumentUploadViewSet)
router.register("images", views.ImageUploadViewSet)
