import pytest
from django.urls import reverse
from rest_framework import status

from eventos2.core.models import EventRegistration, Submission


@pytest.mark.django_db
def test_submit_valid(
    api_client, track_factory, event_factory, user_factory,
):
    # DADO um usuário autenticado, um evento no qual ele está registrado,
    # e um track no evento.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    EventRegistration.objects.create(event=event, user=user)
    track = track_factory(event=event, name="Track A")
    # E DADO um segundo usuário.
    other_user = user_factory(name="other-user", permissions=[])

    # QUANDO a API é chamada para submeter no track.
    resp = api_client.post(
        reverse("submission-list"),
        {"track": track.id, "title": "Title", "other_authors": [other_user.public_id]},
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
    # DADO um usuário autenticado, um evento no qual ele não está registrado,
    # e um track no evento.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    track = track_factory(event=event, name="Track A")

    # QUANDO a API é chamada para submeter no track.
    resp = api_client.post(
        reverse("submission-list"), {"track": track.id, "title": "Title"}
    )

    # ENTÃO a reposta deve ser de falta de permissões
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO o submission não deve ser criado.
    assert Submission.objects.count() == 0


@pytest.mark.django_db
def test_submit_out_of_submission_period(
    api_client,
    track_factory,
    event_factory,
    user_factory,
    freezer,
    parse_to_aware_datetime,
):
    # DADO um usuário autenticado, um evento no qual ele está registrado,
    # e um track no evento.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event = event_factory(
        slug="event-a",
        owners=[],
        starts_on=parse_to_aware_datetime("2020-01-01"),
        ends_on=parse_to_aware_datetime("2020-02-02"),
    )
    EventRegistration.objects.create(event=event, user=user)
    track = track_factory(
        event=event, name="Track A", starts_on=event.starts_on, ends_on=event.ends_on
    )
    # E DADO que já passou o tempo de submissão
    freezer.move_to(parse_to_aware_datetime("2020-03-03"))

    # QUANDO a API é chamada para submeter no track.
    resp = api_client.post(
        reverse("submission-list"), {"track": track.id, "title": "Title"}
    )

    # ENTÃO a reposta de falha deve conter o erro no campo track.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["track"]) != 0
    # E ENTÃO o submission não deve ser criado.
    assert Submission.objects.count() == 0
