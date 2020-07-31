from django.db import models
from django.utils import timezone

from eventos2.core.models.event import Event, EventRegistration
from eventos2.core.models.soft_deletion import SoftDeletableModel
from eventos2.core.models.user import User


class Activity(SoftDeletableModel):
    event = models.ForeignKey(
        Event, on_delete=models.PROTECT, related_name="activities"
    )
    slug = models.CharField(
        max_length=255, unique=True, help_text="A unique, readable identifier"
    )
    name = models.CharField(
        max_length=255, help_text="The activity's name in its native language"
    )
    name_english = models.CharField(
        max_length=255, blank=True, help_text="The activity's name in english"
    )
    starts_on = models.DateTimeField()
    ends_on = models.DateTimeField()

    owners = models.ManyToManyField(
        User, through="ActivityOwnership", related_name="activities_owned"
    )

    def is_open_on(self, date):
        return self.starts_on <= date <= self.ends_on

    @property
    def is_open(self):
        return self.is_open_on(timezone.now())

    class Meta:
        permissions = [
            ("register_self_into_activity", "Can self-register into an activity"),
        ]


class ActivityOwnership(models.Model):
    activity = models.ForeignKey(
        Activity, on_delete=models.PROTECT, related_name="ownerships"
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="activity_ownerships"
    )


class ActivityRegistration(models.Model):
    activity = models.ForeignKey(
        Activity, on_delete=models.PROTECT, related_name="registrations"
    )
    event_registration = models.ForeignKey(
        EventRegistration,
        on_delete=models.PROTECT,
        related_name="activity_registrations",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["activity", "event_registration"],
                name="unique_activity_registration",
            )
        ]
