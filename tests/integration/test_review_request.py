import pytest
from django.urls import reverse
from rest_framework import status

from eventos2.core.models import EventRegistration, Review


@pytest.mark.django_db
def test_create_valid(
    api_client,
    track_factory,
    event_factory,
    user_factory,
    track_review_question_factory,
    track_submission_document_slot_factory,
    document_factory,
    submission_factory,
):
    # DADO um usuário autenticado, que é o event owner,
    # outro que fez a submission, e outro que será o reviewer.
    event_owner_user = user_factory(name="user_a", permissions=[])
    submitter_user = user_factory(name="user_b", permissions=[])
    reviewer_user = user_factory(name="user_c", permissions=[])
    api_client.force_authenticate(user=event_owner_user)
    # E DADO um evento no qual ambos estão registrados.
    event = event_factory(slug="event-a", owners=[event_owner_user])
    EventRegistration.objects.create(event=event, user=submitter_user)
    EventRegistration.objects.create(event=event, user=reviewer_user)
    # E DADO um track.
    track = track_factory(event=event, name="Track A")
    # E DADO uma submission.
    submission = submission_factory(
        track=track, title="Submission A", authors=[submitter_user]
    )

    # QUANDO a API é chamada para fazer a review request.
    resp = api_client.post(
        reverse("review-request-list"),
        {"submission": submission.id, "author": reviewer_user.public_id},
    )

    # ENTÃO a reposta deve ser de sucesso
    assert resp.status_code == status.HTTP_201_CREATED
    # E ENTÃO a review deve ser criada.
    assert Review.objects.count() == 1
    assert Review.objects.first().author == reviewer_user
    assert Review.objects.first().submission == submission
    assert Review.objects.first().is_pending


@pytest.mark.django_db
def test_create_unauthorized(
    api_client,
    track_factory,
    event_factory,
    user_factory,
    track_review_question_factory,
    track_submission_document_slot_factory,
    document_factory,
    submission_factory,
):
    # DADO um usuário autenticado, que será o reviewer, e um outro que fez a submission.
    reviewer_user = user_factory(name="user_a", permissions=[])
    submitter_user = user_factory(name="user_b", permissions=[])
    api_client.force_authenticate(user=reviewer_user)
    # E DADO um evento no qual ambos estão registrados.
    event = event_factory(slug="event-a", owners=[])
    EventRegistration.objects.create(event=event, user=reviewer_user)
    EventRegistration.objects.create(event=event, user=submitter_user)
    # E DADO um track.
    track = track_factory(event=event, name="Track A")
    # E DADO uma submission.
    submission = submission_factory(
        track=track, title="Submission A", authors=[submitter_user]
    )

    # QUANDO a API é chamada para fazer a review request.
    resp = api_client.post(
        reverse("review-request-list"),
        {"submission": submission.id, "author": reviewer_user.public_id},
    )

    # ENTÃO a reposta deve ser de falta de permissões
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO a review não deve ser criada.
    assert Review.objects.count() == 0
