from django.db import models
from django.utils import timezone

from eventos2.core.models.event import Event
from eventos2.core.models.soft_deletion import SoftDeletableModel


class Track(SoftDeletableModel):
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name="tracks")
    name = models.CharField(
        max_length=255, help_text="The track's name in its native language"
    )
    name_english = models.CharField(
        max_length=255, blank=True, help_text="The track's name in english"
    )
    starts_on = models.DateTimeField()
    ends_on = models.DateTimeField()

    def is_open_on(self, date):
        return self.starts_on <= date <= self.ends_on

    @property
    def is_open(self):
        return self.is_open_on(timezone.now())

    class Meta:
        permissions = [
            ("add_submission_to_track", "Can add a submission to a track"),
            (
                "view_review_questions_for_track",
                "Can view review questions for a track",
            ),
        ]


class TrackSubmissionDocumentSlot(models.Model):
    track = models.ForeignKey(
        Track, on_delete=models.PROTECT, related_name="submission_document_slots"
    )
    name = models.CharField(
        max_length=255, help_text="The slot's name in its native language"
    )
    name_english = models.CharField(
        max_length=255, blank=True, help_text="The slot's name in english"
    )
    starts_on = models.DateTimeField()
    ends_on = models.DateTimeField()

    def is_open_on(self, date):
        return self.starts_on <= date <= self.ends_on

    @property
    def is_open(self):
        return self.is_open_on(timezone.now())

    @property
    def event(self):  # pragma: no cover - no complexity
        return self.track.event


class TrackReviewQuestion(models.Model):
    class AnswerType(models.TextChoices):
        YES_NO = "yes_no"
        GRADE_ZERO_TO_TEN = "grade_zero_to_ten"
        TEXT = "text"

    track = models.ForeignKey(
        Track, on_delete=models.PROTECT, related_name="review_questions"
    )
    text = models.CharField(max_length=255)
    answer_type = models.CharField(max_length=255, choices=AnswerType.choices)

    @property
    def event(self):  # pragma: no cover - no complexity
        return self.track.event
