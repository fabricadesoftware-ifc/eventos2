from django.db import models

from eventos2.core.models.soft_deletion import SoftDeletableModel
from eventos2.images.models import Image


class Event(SoftDeletableModel):
    name = models.CharField(
        max_length=255, help_text="The event's name in its native language"
    )
    name_english = models.CharField(
        max_length=255, blank=True, help_text="The event's name in english"
    )
    starts_on = models.DateTimeField()
    ends_on = models.DateTimeField()
    logo = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="+", blank=True, null=True
    )

    def __str__(self):
        return self.name
