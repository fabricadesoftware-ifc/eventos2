from rest_framework.routers import SimpleRouter

from eventos2.core import views

router = SimpleRouter()
router.register(r"activities", views.ActivityViewSet, basename="activity")
router.register(
    r"activity_registrations",
    views.ActivityRegistrationViewSet,
    basename="activity-registration",
)
router.register(r"events", views.EventViewSet, basename="event")
router.register(
    r"event_registrations",
    views.EventRegistrationViewSet,
    basename="event-registration",
)
router.register(r"reviews", views.ReviewViewSet, basename="review")
router.register(r"submissions", views.SubmissionViewSet, basename="submission")
router.register(
    r"submission_documents",
    views.SubmissionDocumentViewSet,
    basename="submission-document",
)
router.register(r"tracks", views.TrackViewSet, basename="track")
router.register(
    r"track_review_questions",
    views.TrackReviewQuestionViewSet,
    basename="track-review-question",
)
router.register(r"tracks", views.TrackViewSet, basename="track")
router.register(
    r"track_submission_document_slots",
    views.TrackSubmissionDocumentSlotViewSet,
    basename="track-submission-document-slot",
)
router.register(r"users", views.UserViewSet, basename="user")
