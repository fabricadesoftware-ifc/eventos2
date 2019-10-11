from django.db import models

from core.models.soft_deletion import SoftDeletableModel
from images.models import Image


class Event(SoftDeletableModel):
    name = models.CharField(
        max_length=255, help_text="The event's name in its native language"
    )
    name_english = models.CharField(
        max_length=255, blank=True, help_text="The event's name in english"
    )
    starts_on = models.DateTimeField()
    ends_on = models.DateTimeField()
    location = models.CharField(
        max_length=255, help_text="Where the event will take place"
    )
    logo = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="+", blank=True, null=True
    )

    def __str__(self):
        return self.name


class SponsorshipCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Sponsorship(models.Model):
    sponsored_event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="sponsorships",
        related_query_name="sponsorship",
    )
    sponsor = models.CharField(
        max_length=255,
        help_text="The individual or organization who is sponsoring the event",
    )
    category = models.ForeignKey(SponsorshipCategory, on_delete=models.PROTECT)

    def __str__(self):
        return "{:s} by {:s}".format(self.category.name, self.sponsor)
