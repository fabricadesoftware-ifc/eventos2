from rest_framework.routers import DefaultRouter

from core import views

app_name = "core"

router = DefaultRouter()
router.register(r"event", views.EventViewSet)
router.register(r"sponsorship", views.SponsorshipViewSet)
router.register(r"sponsorship_category", views.SponsorshipCategoryViewSet)
router.register(r"image", views.ImageUploadViewSet)

urlpatterns = router.urls
