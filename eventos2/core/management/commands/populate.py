import random
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from eventos2.core.models import (
    Activity,
    ActivityRegistration,
    Event,
    EventRegistration,
    Submission,
    Track,
    TrackSubmissionDocumentSlot,
    User,
)


class Command(BaseCommand):
    help = "Creates example data"

    def handle(self, *args, **options):
        n_users = 9
        n_activities = 9
        n_tracks = 9
        n_min_slots_per_track = 1
        n_max_slots_per_track = 3
        n_min_authors_per_submission = 1
        n_max_authors_per_submission = 3
        n_registered_users = int(n_users * 0.5)

        superuser = User.objects.filter(is_superuser=True).first()
        if not superuser:
            raise CommandError(
                "You must create a superuser before running this command."
            )

        event = self._create_event()
        event.owners.add(superuser)

        users = [self._create_user(i + 1) for i in range(n_users)]
        activities = [self._create_activity(event, i + 1) for i in range(n_activities)]

        tracks = [self._create_track(event, i + 1) for i in range(n_tracks)]
        for track in tracks:
            n_slots = random.randrange(  # nosec
                n_min_slots_per_track, n_max_slots_per_track + 1
            )
            [
                self._create_track_submission_document_slot(track, i + 1)
                for i in range(n_slots)
            ]

        track_authors_pairs = []

        for _ in range(n_tracks):
            track = random.choice(tracks)  # nosec
            n_authors = random.randrange(  # nosec
                n_min_authors_per_submission, n_max_authors_per_submission + 1
            )
            authors = random.sample(users, n_authors)
            track_authors_pairs.append((track, authors))

        for track, authors in track_authors_pairs:
            self._create_submission(track, authors)

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
        starts_on = event.starts_on
        ends_on = event.ends_on
        if n % 2 == 0:
            starts_on += timedelta(days=1)
        elif n % 3 == 0:
            ends_on = starts_on + timedelta(minutes=5)
        return Activity.objects.create(
            event=event,
            name="Atividade {}".format(n),
            name_english="Activity {}".format(n),
            slug="atividade-{}".format(n),
            starts_on=starts_on,
            ends_on=ends_on,
        )

    @staticmethod
    def _create_track(event, n):
        starts_on = event.starts_on
        ends_on = event.ends_on
        if n % 2 == 0:
            starts_on += timedelta(days=1)
        elif n % 3 == 0:
            ends_on = starts_on + timedelta(minutes=5)
        return Track.objects.create(
            event=event,
            name="Track {}".format(n),
            name_english="Track {}".format(n),
            slug="track-{}".format(n),
            starts_on=starts_on,
            ends_on=ends_on,
        )

    @staticmethod
    def _create_track_submission_document_slot(track, n):
        starts_on = track.starts_on
        ends_on = track.ends_on
        if n % 2 == 0:
            starts_on += timedelta(days=1)
        elif n % 3 == 0:
            ends_on = starts_on + timedelta(minutes=5)
        return TrackSubmissionDocumentSlot.objects.create(
            track=track,
            name="Slot {}".format(n),
            name_english="Slot {}".format(n),
            starts_on=starts_on,
            ends_on=ends_on,
        )

    @staticmethod
    def _create_submission(track, authors):
        author_str = ", ".join(
            "{} {}".format(x.first_name, x.last_name) for x in authors
        )
        submission = Submission.objects.create(
            track=track,
            title="Trabalho por {}".format(author_str),
            title_english="Submission by {}".format(author_str),
        )
        submission.authors.add(*authors)
        return submission

    @staticmethod
    def _create_event_registration(event, user):
        return EventRegistration.objects.create(event=event, user=user)

    @staticmethod
    def _create_activity_registration(activity, event_registration):
        return ActivityRegistration.objects.create(
            activity=activity, event_registration=event_registration
        )
