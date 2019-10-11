from rest_framework.routers import DefaultRouter

from images import views

app_name = "images"

router = DefaultRouter()
router.register("", views.ImageUploadViewSet)

urlpatterns = router.urls
