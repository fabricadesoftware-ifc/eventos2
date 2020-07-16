from django.db import models

from eventos2.core.models.soft_deletion import SoftDeletableModel
from eventos2.core.models.user import User
from eventos2.media.models import Image


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

    def __str__(self):  # pragma: no cover - internal use
        return self.name

    class Meta:
        permissions = [
            ("view_registrations_for_event", "Can view registrations for an event"),
            ("view_activities_for_event", "Can view activities for an event"),
            ("view_tracks_for_event", "Can view tracks for an event"),
            (
                "view_activity_registrations_for_event",
                "Can view activity registrations for an event",
            ),
            ("register_self_into_event", "Can self-register into an event"),
        ]


class EventOwnership(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.PROTECT, related_name="ownerships"
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="event_ownerships"
    )


class EventRegistration(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.PROTECT, related_name="registrations"
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="event_registrations"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event", "user"], name="unique_event_registration"
            )
        ]
