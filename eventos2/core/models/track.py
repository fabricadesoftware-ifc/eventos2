from django.db import models

from eventos2.core.models.event import Event
from eventos2.core.models.soft_deletion import SoftDeletableModel


class Track(SoftDeletableModel):
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name="tracks")
    slug = models.CharField(
        max_length=255, unique=True, help_text="A unique, readable identifier"
    )
    name = models.CharField(
        max_length=255, help_text="The track's name in its native language"
    )
    name_english = models.CharField(
        max_length=255, blank=True, help_text="The track's name in english"
    )

    class Meta:
        permissions = [
            ("add_submission_to_track", "Can add a submission to a track"),
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

    @property
    def event(self):  # pragma: no cover - no complexity
        return self.track.event
