from rest_framework.routers import DefaultRouter

from eventos2.images import views

app_name = "images"

router = DefaultRouter()
router.register("image", views.ImageUploadViewSet)
