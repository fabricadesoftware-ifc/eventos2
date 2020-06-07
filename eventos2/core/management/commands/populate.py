import random
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from eventos2.core.models import (
    Activity,
    ActivityRegistration,
    Event,
    EventRegistration,
    User,
)


class Command(BaseCommand):
    help = "Creates example data"

    def handle(self, *args, **options):
        n_users = 10
        n_activities = 10
        n_registered_users = int(n_users * 0.8)

        superuser = User.objects.filter(is_superuser=True).first()
        if not superuser:
            raise CommandError(
                "You must create a superuser before running this command."
            )

        event = self._create_event()
        event.owners.add(superuser)

        users = [self._create_user(i + 1) for i in range(n_users)]
        activities = [self._create_activity(event, i + 1) for i in range(n_activities)]

        event_registrations = [
            self._create_event_registration(event, user)
            for user in random.sample(users, n_registered_users)  # nosec
        ]

        activity_registration_pairs = set(
            (random.choice(activities), random.choice(event_registrations))  # nosec
            for _ in range(n_users * n_activities)
        )
        for activity, event_registration in activity_registration_pairs:
            self._create_activity_registration(activity, event_registration)

        self.stdout.write(self.style.SUCCESS("Successfully populated data."))

    @staticmethod
    def _create_event():
        starts_on = timezone.now()
        ends_on = starts_on + timedelta(days=2)
        return Event.objects.create(
            name="Teste",
            name_english="Test",
            slug="test",
            starts_on=starts_on,
            ends_on=ends_on,
        )

    @staticmethod
    def _create_user(n):
        email = "user{}@example.com".format(n)
        user = User.objects.create(
            email=email, username=email, first_name="User", last_name=str(n)
        )
        user.set_password("user{}".format(n))
        return user

    @staticmethod
    def _create_activity(event, n):
        return Activity.objects.create(
            event=event,
            name="Atividade {}".format(n),
            name_english="Activity {}".format(n),
            slug="atividade-{}".format(n),
            starts_on=event.starts_on,
            ends_on=event.ends_on,
        )

    @staticmethod
    def _create_event_registration(event, user):
        return EventRegistration.objects.create(event=event, user=user)

    @staticmethod
    def _create_activity_registration(activity, event_registration):
        return ActivityRegistration.objects.create(
            activity=activity, event_registration=event_registration
        )
