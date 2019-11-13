from rest_framework.routers import SimpleRouter

from eventos2.core import views

router = SimpleRouter()
router.register(r"event", views.EventViewSet)
router.register(r"event_registration", views.EventRegistrationViewSet)
router.register(r"event_registration_type", views.EventRegistrationTypeViewSet)
router.register(r"user", views.UserViewSet)
