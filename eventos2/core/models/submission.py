from django.db import models

from eventos2.core.models.soft_deletion import SoftDeletableModel
from eventos2.core.models.track import Track, TrackSubmissionDocumentSlot
from eventos2.core.models.user import User
from eventos2.media.models import Document


class Submission(SoftDeletableModel):
    track = models.ForeignKey(
        Track, on_delete=models.PROTECT, related_name="submissions"
    )
    title = models.CharField(
        max_length=255, help_text="The submission's name in its native language"
    )
    title_english = models.CharField(
        max_length=255, blank=True, help_text="The submission's name in english"
    )
    authors = models.ManyToManyField(
        User, through="SubmissionAuthorship", related_name="submissions_authored"
    )

    @property
    def event(self):  # pragma: no cover - no complexity
        return self.track.event


class SubmissionAuthorship(models.Model):
    submission = models.ForeignKey(
        Submission, on_delete=models.PROTECT, related_name="authorships"
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="submission_authorships"
    )


class SubmissionDocument(models.Model):
    slot = models.ForeignKey(
        TrackSubmissionDocumentSlot, on_delete=models.PROTECT, related_name="documents",
    )
    submission = models.ForeignKey(
        Submission, on_delete=models.PROTECT, related_name="documents"
    )

    document = models.ForeignKey(Document, on_delete=models.PROTECT, related_name="+")
    submitted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["slot", "submission"], name="unique_submission_document"
            )
        ]
