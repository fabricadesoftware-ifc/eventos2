import pytest
from django.urls import reverse
from rest_framework import status

from eventos2.core.models import TrackReviewQuestion


@pytest.mark.django_db
def test_create_valid(api_client, user_factory, event_factory, track_factory):
    # DADO um usuário autenticado, um evento pertencente a ele, e um track no evento.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[user])
    track = track_factory(event=event, name="Track A")

    # E DADO dados de question válidos.
    # QUANDO a API é chamada.
    resp = api_client.post(
        reverse("track-review-question-list"),
        {"track": track.id, "text": "Question A", "answer_type": "text"},
    )

    # ENTÃO a resposta de sucesso deve conter os dados da question.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["text"] == "Question A"
    # E ENTÃO a question deve existir.
    assert TrackReviewQuestion.objects.get(id=resp.data["id"]).text == "Question A"


@pytest.mark.django_db
def test_create_unauthorized(api_client, user_factory, event_factory, track_factory):
    # DADO um usuário autenticado, um evento não pertencente a ele,
    # e um track no evento.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    track = track_factory(event=event, name="Track A")

    # E DADO dados de question válidos.
    # QUANDO a API é chamada.
    resp = api_client.post(
        reverse("track-review-question-list"),
        {"track": track.id, "text": "Question A", "answer_type": "text"},
    )

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO a question não deve ser criada.
    assert TrackReviewQuestion.objects.count() == 0


@pytest.mark.django_db
def test_update_valid(
    api_client,
    user_factory,
    event_factory,
    track_factory,
    track_review_question_factory,
):
    # DADO um usuário autenticado, um evento pertencente a ele, e um track no evento.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[user])
    track = track_factory(
        event=event, name="Track A", starts_on=event.starts_on, ends_on=event.ends_on
    )
    # E DADO uma question existente no track.
    question = track_review_question_factory(track=track, text="Question A")

    # E DADO dados de question válidos.
    # QUANDO a API é chamada.
    resp = api_client.put(
        reverse("track-review-question-detail", args=[question.id]),
        {
            "text": "{} modified!".format(question.text),
            "answer_type": question.answer_type,
        },
    )

    # ENTÃO a reposta de sucesso deve conter a question modificada.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["text"] == "{} modified!".format(question.text)
    # E ENTÃO a question deve ser modificada.
    assert TrackReviewQuestion.objects.get(
        pk=question.id
    ).text == "{} modified!".format(question.text)
    assert TrackReviewQuestion.objects.count() == 1


@pytest.mark.django_db
def test_update_unauthorized(
    api_client,
    user_factory,
    event_factory,
    track_factory,
    track_review_question_factory,
):
    # DADO um usuário autenticado, um evento não pertencente a ele,
    # e um track no evento.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    track = track_factory(event=event, name="Track A")
    # E DADO uma question existente no track.
    question = track_review_question_factory(track=track, text="Question A")

    # E DADO dados de question válidos.
    # QUANDO a API é chamada.
    resp = api_client.put(
        reverse("track-review-question-detail", args=[question.id]),
        {
            "text": "{} modified!".format(question.text),
            "answer_type": question.answer_type,
        },
    )

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO a question não deve ser modificado.
    assert TrackReviewQuestion.objects.get(pk=question.id).text == question.text


@pytest.mark.django_db
def test_delete_valid(
    api_client,
    user_factory,
    event_factory,
    track_factory,
    track_review_question_factory,
):
    # DADO um usuário autenticado, um evento pertencente a ele, e um track no evento.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[user])
    track = track_factory(event=event, name="Track A")
    # E DADO uma question existente no track.
    question = track_review_question_factory(track=track, text="Question A")

    # QUANDO a API é chamada para deletar a question.
    delete_resp = api_client.delete(
        reverse("track-review-question-detail", args=[question.id])
    )

    # ENTÃO a deleção deverá ter sucesso.
    assert delete_resp.status_code == status.HTTP_204_NO_CONTENT
    # E ENTÃO a question não existirá.
    assert TrackReviewQuestion.objects.count() == 0


@pytest.mark.django_db
def test_delete_unauthorized(
    api_client,
    user_factory,
    event_factory,
    track_factory,
    track_review_question_factory,
):
    # DADO um usuário autenticado, um evento não pertencente a ele,
    # e um track no evento.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    track = track_factory(event=event, name="Track A")
    # E DADO uma question existente no track.
    question = track_review_question_factory(track=track, text="Question A")

    # QUANDO a API é chamada para deletar a question.
    resp = api_client.delete(
        reverse("track-review-question-detail", args=[question.id])
    )

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO a question não deve ser deletada.
    assert TrackReviewQuestion.objects.count() == 1
