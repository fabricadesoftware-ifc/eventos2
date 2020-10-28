import pytest
from django.urls import reverse
from rest_framework import status

from eventos2.core.models import EventRegistration, Review, ReviewAnswer


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
    review_factory,
):
    # DADO um usuário autenticado, que fez a submission, e um outro que fará o review.
    submitter_user = user_factory(name="user_b", permissions=[])
    reviewer_user = user_factory(name="user_a", permissions=[])
    api_client.force_authenticate(user=reviewer_user)
    # E DADO um evento no qual ambos estão registrados.
    event = event_factory(slug="event-a", owners=[])
    EventRegistration.objects.create(event=event, user=submitter_user)
    EventRegistration.objects.create(event=event, user=reviewer_user)
    # E DADO um track com uma question.
    track = track_factory(event=event, name="Track A")
    question = track_review_question_factory(track=track, text="Question A")
    # E DADO uma submission.
    submission = submission_factory(
        track=track, title="Submission A", authors=[submitter_user]
    )
    # E DADO uma review pendente.
    pending_review = review_factory(submission=submission, author=reviewer_user)

    # QUANDO a API é chamada para fazer a review.
    resp = api_client.post(
        reverse("review-list"),
        {
            "request": pending_review.id,
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
    review_factory,
):
    # DADO dois usuários, um deles autenticado.
    user_a = user_factory(name="User A", permissions=[])
    user_b = user_factory(name="User B", permissions=[])
    api_client.force_authenticate(user=user_a)
    # E DADO um evento no qual ambos estão registrados.
    event = event_factory(slug="event-a", owners=[])
    EventRegistration.objects.create(event=event, user=user_a)
    EventRegistration.objects.create(event=event, user=user_b)
    # E DADO um track com uma question.
    track = track_factory(event=event, name="Track A")
    question = track_review_question_factory(track=track, text="Question A")
    # E DADO uma submission pelo user A.
    submission = submission_factory(track=track, title="Submission A", authors=[user_a])
    # E DADO uma review pendente direcionada ao user B.
    pending_review = review_factory(submission=submission, author=user_b)

    # QUANDO a API é chamada para fazer a review pelo user A.
    resp = api_client.post(
        reverse("review-list"),
        {
            "request": pending_review.id,
            "answers": [{"question": question.id, "text": "Answer A"}],
        },
    )

    # ENTÃO a reposta de falha deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO a review não deve ser completa.
    assert Review.objects.get(pk=pending_review.pk).is_pending


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
    review_factory,
):
    # DADO um usuário autenticado, que fez a submission, e um outro que fará o review.
    submitter_user = user_factory(name="user_b", permissions=[])
    reviewer_user = user_factory(name="user_a", permissions=[])
    api_client.force_authenticate(user=reviewer_user)
    # E DADO um evento no qual ambos estão registrados.
    event = event_factory(slug="event-a", owners=[])
    EventRegistration.objects.create(event=event, user=submitter_user)
    EventRegistration.objects.create(event=event, user=reviewer_user)
    # E DADO um track com uma question.
    track = track_factory(event=event, name="Track A")
    question_a = track_review_question_factory(track=track, text="Question A")
    track_review_question_factory(track=track, text="Question B")
    # E DADO uma submission.
    submission = submission_factory(
        track=track, title="Submission A", authors=[submitter_user]
    )
    # E DADO uma review pendente.
    pending_review = review_factory(submission=submission, author=reviewer_user)

    # QUANDO a API é chamada para fazer a review.
    resp = api_client.post(
        reverse("review-list"),
        {
            "request": pending_review.id,
            "answers": [{"question": question_a.id, "text": "Answer A"}],
        },
    )

    # ENTÃO a reposta de falha deve conter o erro no campo answers,
    # pois a question A não foi respondida.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["answers"]) != 0
    # E ENTÃO a review não deve ser completa.
    assert Review.objects.get(pk=pending_review.pk).is_pending


@pytest.mark.django_db
def test_create_duplicate(
    api_client,
    track_factory,
    event_factory,
    user_factory,
    track_review_question_factory,
    track_submission_document_slot_factory,
    document_factory,
    submission_factory,
    review_factory,
):
    # DADO um usuário autenticado, que fez a submission, e um outro que fará o review.
    submitter_user = user_factory(name="user_b", permissions=[])
    reviewer_user = user_factory(name="user_a", permissions=[])
    api_client.force_authenticate(user=reviewer_user)
    # E DADO um evento no qual ambos estão registrados.
    event = event_factory(slug="event-a", owners=[])
    EventRegistration.objects.create(event=event, user=submitter_user)
    EventRegistration.objects.create(event=event, user=reviewer_user)
    # E DADO um track com uma question.
    track = track_factory(event=event, name="Track A")
    question_a = track_review_question_factory(track=track, text="Question A")
    track_review_question_factory(track=track, text="Question B")
    # E DADO uma submission.
    submission = submission_factory(
        track=track, title="Submission A", authors=[submitter_user]
    )
    # E DADO uma review já respondida.
    review = review_factory(submission=submission, author=reviewer_user)
    ReviewAnswer.objects.create(review=review, question=question_a, text="Answer A")

    # QUANDO a API é chamada para fazer a review novamente.
    resp = api_client.post(
        reverse("review-list"),
        {
            "request": review.id,
            "answers": [{"question": question_a.id, "text": "Answer A"}],
        },
    )

    # ENTÃO a reposta de falha deve conter o erro no campo request,
    # pois a review já está completa.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["request"]) != 0
