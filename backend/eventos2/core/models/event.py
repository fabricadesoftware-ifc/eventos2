from django.db import models

from eventos2.core.models.soft_deletion import SoftDeletableModel
from eventos2.core.models.user import User
from eventos2.images.models import Image


class Event(SoftDeletableModel):
    slug = models.CharField(
        max_length=255, unique=True, help_text="A unique, readable identifier"
    )
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
    owners = models.ManyToManyField(
        User, through="EventOwnership", related_name="events_owned"
    )

    def __str__(self):
        return self.name


class EventOwnership(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.PROTECT, related_name="ownerships"
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="event_ownerships"
    )


class EventRegistrationType(models.Model):
    name = models.CharField(max_length=255)
    name_english = models.CharField(max_length=255, blank=True)
    event = models.ForeignKey(
        Event, on_delete=models.PROTECT, related_name="registration_types"
    )
    registrations = models.ManyToManyField(
        User, through="EventRegistration", related_name="event_registrations"
    )

    def __str__(self):
        return self.name


class EventRegistration(models.Model):
    registration_type = models.ForeignKey(
        EventRegistrationType, on_delete=models.PROTECT
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)
