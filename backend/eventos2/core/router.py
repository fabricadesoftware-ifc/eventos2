from rest_framework.routers import DefaultRouter

from eventos2.core import views

router = DefaultRouter()
router.register(r"event", views.EventViewSet)
router.register(r"event_registration", views.EventRegistrationViewSet)
router.register(r"user", views.UserViewSet)
