from django.db import models

from eventos2.core.models.soft_deletion import SoftDeletableModel
from eventos2.core.models.track import Track
from eventos2.core.models.user import User


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


class SubmissionAuthorship(models.Model):
    submission = models.ForeignKey(
        Submission, on_delete=models.PROTECT, related_name="authorships"
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="submission_authorships"
    )
