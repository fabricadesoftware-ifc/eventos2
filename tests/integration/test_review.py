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
    # DADO um usuário autenticado, que fez a submission, e um outro que fará o review.
    submitter_user = user_factory(name="user_b", permissions=[])
    reviewer_user = user_factory(name="user_a", permissions=[])
    api_client.force_authenticate(user=reviewer_user)
    # E DADO um evento no qual ambos estão registrados.
    event = event_factory(slug="event-a", owners=[reviewer_user])
    EventRegistration.objects.create(event=event, user=submitter_user)
    EventRegistration.objects.create(event=event, user=reviewer_user)
    # E DADO um track com uma question.
    track = track_factory(event=event, name="Track A")
    question = track_review_question_factory(track=track, text="Question A")
    # E DADO uma submission.
    submission = submission_factory(
        track=track, title="Submission A", authors=[submitter_user]
    )

    # QUANDO a API é chamada para fazer a review.
    resp = api_client.post(
        reverse("review-list"),
        {
            "submission": submission.id,
            "answers": [{"question": question.id, "text": "Answer A"}],
        },
    )

    # ENTÃO a reposta deve ser de sucesso
    assert resp.status_code == status.HTTP_201_CREATED
    # E ENTÃO a review deve ser criada.
    assert Review.objects.count() == 1
    assert Review.objects.first().author == reviewer_user
    assert Review.objects.first().submission == submission
    assert Review.objects.first().answers.first().text == "Answer A"


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
    # DADO um usuário autenticado.
    user = user_factory(name="user_b", permissions=[])
    api_client.force_authenticate(user=user)
    # E DADO um evento no qual ambos estão registrados.
    event = event_factory(slug="event-a", owners=[])
    EventRegistration.objects.create(event=event, user=user)
    # E DADO um track com uma question.
    track = track_factory(event=event, name="Track A")
    question = track_review_question_factory(track=track, text="Question A")
    # E DADO uma submission.
    submission = submission_factory(track=track, title="Submission A", authors=[user])

    # QUANDO a API é chamada para fazer a review.
    resp = api_client.post(
        reverse("review-list"),
        {
            "submission": submission.id,
            "answers": [{"question": question.id, "text": "Answer A"}],
        },
    )

    # ENTÃO a reposta deve ser de falta de permissões,
    # pois o usuário tem permissões para fazer o review da sua própria submissão.
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO a review não deve ser criada.
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_create_missing_answer(
    api_client,
    track_factory,
    event_factory,
    user_factory,
    track_review_question_factory,
    track_submission_document_slot_factory,
    document_factory,
    submission_factory,
):
    # DADO um usuário autenticado, que fez a submission, e um outro que fará o review.
    submitter_user = user_factory(name="user_b", permissions=[])
    reviewer_user = user_factory(name="user_a", permissions=[])
    api_client.force_authenticate(user=reviewer_user)
    # E DADO um evento no qual ambos estão registrados.
    event = event_factory(slug="event-a", owners=[reviewer_user])
    EventRegistration.objects.create(event=event, user=submitter_user)
    EventRegistration.objects.create(event=event, user=reviewer_user)
    # E DADO um track com uma question.
    track = track_factory(event=event, name="Track A")
    track_review_question_factory(track=track, text="Question A")
    # E DADO uma submission.
    submission = submission_factory(
        track=track, title="Submission A", authors=[submitter_user]
    )

    # QUANDO a API é chamada para fazer a review.
    resp = api_client.post(
        reverse("review-list"), {"submission": submission.id, "answers": []},
    )

    # ENTÃO a reposta de falha deve conter o erro no campo answers,
    # pois a question A não foi respondida.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["answers"]) != 0
    # E ENTÃO a review não deve ser criada.
    assert Review.objects.count() == 0
