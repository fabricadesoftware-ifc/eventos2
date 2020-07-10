import pytest
from django.urls import reverse
from rest_framework import status

from eventos2.core.models import EventRegistration, Submission


@pytest.mark.django_db
def test_submit_valid(api_client, track_factory, event_factory, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento no qual o usuário está registrado.
    event = event_factory(slug="event-a", owners=[])
    EventRegistration.objects.create(event=event, user=user)

    # E DADO um track.
    track = track_factory(event=event, slug="track-a")

    # E DADO um segundo usuário
    other_user = user_factory(name="other-user", permissions=[])

    # QUANDO a API é chamada para submeter no track.
    resp = api_client.post(
        reverse("submission-list"),
        {
            "track": track.slug,
            "title": "Title",
            "other_authors": [other_user.public_id],
        },
    )

    # ENTÃO a reposta deve ser de sucesso
    assert resp.status_code == status.HTTP_201_CREATED

    # E ENTÃO o submission deve ser criado.
    assert Submission.objects.count() == 1
    assert Submission.objects.first().authors.count() == 2


@pytest.mark.django_db
def test_submit_not_registered_to_event(
    api_client, track_factory, event_factory, user_factory
):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento no qual o usuário não está registrado.
    event = event_factory(slug="event-a", owners=[])

    # E DADO um track.
    track = track_factory(event=event, slug="track-a")

    # QUANDO a API é chamada para submeter no track.
    resp = api_client.post(
        reverse("submission-list"), {"track": track.slug, "title": "Title"}
    )

    # ENTÃO a reposta deve ser de falta de permissões
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # E ENTÃO o submission não deve ser criado.
    assert Submission.objects.count() == 0
