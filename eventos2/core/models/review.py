from django.db import models

from eventos2.core.models.submission import Submission
from eventos2.core.models.track import TrackReviewQuestion
from eventos2.core.models.user import User


class Review(models.Model):
    submission = models.ForeignKey(
        Submission, on_delete=models.PROTECT, related_name="reviews"
    )
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="reviews")

    @property
    def is_pending(self):
        return self.answers.count() == 0

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["submission", "author"], name="unique_review"
            )
        ]


class ReviewAnswer(models.Model):
    review = models.ForeignKey(Review, on_delete=models.PROTECT, related_name="answers")
    question = models.ForeignKey(
        TrackReviewQuestion, on_delete=models.PROTECT, related_name="answers"
    )
    text = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["review", "question"], name="unique_review_answer"
            )
        ]
