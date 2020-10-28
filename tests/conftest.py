from datetime import timedelta

import dateutil
import pytest
from django.contrib.auth.models import Permission
from django.utils import timezone
from rest_framework.test import APIClient

from eventos2.core.models import (
    Activity,
    Event,
    Review,
    Submission,
    Track,
    TrackReviewQuestion,
    TrackSubmissionDocumentSlot,
    User,
)
from eventos2.media.models import Document


@pytest.fixture()
def api_client():
    """
    Instancia de cliente para teste do DRF.
    Faz requests com JSON, em vez de multipart/form-data.
    (como definido nas settings, REST_FRAMEWORK.TEST_REQUEST_DEFAULT_FORMAT)
    """
    return APIClient()


@pytest.fixture
def user_factory():
    def _factory(*, name, permissions):
        user = User.objects.create(email="{0}@example.com".format(name), username=name)
        user.set_password(name)
        user.save()

        for permission in permissions:
            app_label, codename = permission.split(".")
            user.user_permissions.add(
                Permission.objects.get(
                    content_type__app_label=app_label, codename=codename
                )
            )

        return user

    return _factory


@pytest.fixture
def event_factory():
    def _factory(*, slug, owners, starts_on=None, ends_on=None):
        default_starts_on = timezone.now()
        default_ends_on = default_starts_on + timedelta(days=10)
        event = Event.objects.create(
            slug=slug,
            name=slug,
            starts_on=starts_on or default_starts_on,
            ends_on=ends_on or default_ends_on,
        )
        event.owners.add(*owners)
        return event

    return _factory


@pytest.fixture
def activity_factory():
    def _factory(*, event, name, owners, starts_on=None, ends_on=None):
        default_starts_on = timezone.now()
        default_ends_on = default_starts_on + timedelta(days=10)
        activity = Activity.objects.create(
            event=event,
            name=name,
            starts_on=starts_on or default_starts_on,
            ends_on=ends_on or default_ends_on,
        )
        activity.owners.add(*owners)
        return activity

    return _factory


@pytest.fixture
def submission_factory():
    def _factory(*, track, title, authors):
        submission = Submission.objects.create(track=track, title=title,)
        submission.authors.add(*authors)
        return submission

    return _factory


@pytest.fixture
def review_factory():
    def _factory(*, submission, author):
        review = Review.objects.create(submission=submission, author=author)
        return review

    return _factory


@pytest.fixture
def track_factory():
    def _factory(*, event, name, starts_on=None, ends_on=None):
        default_starts_on = timezone.now()
        default_ends_on = default_starts_on + timedelta(days=10)
        track = Track.objects.create(
            event=event,
            name=name,
            starts_on=starts_on or default_starts_on,
            ends_on=ends_on or default_ends_on,
        )
        return track

    return _factory


@pytest.fixture
def track_review_question_factory():
    def _factory(*, track, text, answer_type=TrackReviewQuestion.AnswerType.TEXT):
        question = TrackReviewQuestion.objects.create(
            track=track, text=text, answer_type=answer_type
        )
        return question

    return _factory


@pytest.fixture
def track_submission_document_slot_factory():
    def _factory(*, track, name, starts_on=None, ends_on=None):
        default_starts_on = timezone.now()
        default_ends_on = default_starts_on + timedelta(days=10)
        slot = TrackSubmissionDocumentSlot.objects.create(
            track=track,
            name=name,
            starts_on=starts_on or default_starts_on,
            ends_on=ends_on or default_ends_on,
        )
        return slot

    return _factory


@pytest.fixture
def document_factory():
    def _factory(*, file_path, content_type):
        document = Document.objects.create(file=file_path, content_type=content_type,)
        return document

    return _factory


@pytest.fixture
def parse_to_aware_datetime():
    def _func(s):
        return timezone.make_aware(dateutil.parser.parse(s))

    return _func
