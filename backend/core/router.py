from rest_framework.routers import DefaultRouter

from core import views

router = DefaultRouter()
router.register(r"event", views.EventViewSet)
router.register(r"sponsorship", views.SponsorshipViewSet)
router.register(r"sponsorship_category", views.SponsorshipCategoryViewSet)
router.register(r"user", views.UserViewSet)
