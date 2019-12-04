from rest_framework.routers import SimpleRouter

from eventos2.core import views

router = SimpleRouter()
router.register(r"events", views.EventViewSet, basename="event")
router.register(r"event_registrations", views.EventRegistrationViewSet)
router.register(r"event_registration_types", views.EventRegistrationTypeViewSet)
router.register(r"users", views.UserViewSet)
