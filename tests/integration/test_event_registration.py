import pytest
from django.urls import reverse
from rest_framework import status

from eventos2.core.models import EventRegistration


@pytest.mark.django_db
def test_register_valid(api_client, user_factory, event_factory):
    # DADO um usuário autenticado, e um evento.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])

    # QUANDO a API é chamada para registrar o usuário no evento.
    resp = api_client.post(
        reverse("event-registration-list"), {"event_slug": event.slug}
    )

    # ENTÃO a reposta deve ser de sucesso
    assert resp.status_code == status.HTTP_200_OK
    # E ENTÃO a registration deve ser criado.
    assert EventRegistration.objects.count() == 1
    assert EventRegistration.objects.first().user == user


@pytest.mark.django_db
def test_register_duplicate(api_client, user_factory, event_factory):
    # DADO um usuário autenticado, um evento no qual ele está registrado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    EventRegistration.objects.create(event=event, user=user)

    # QUANDO a API é chamada para registrar o usuário no evento novamente.
    resp = api_client.post(
        reverse("event-registration-list"), {"event_slug": event.slug}
    )

    # ENTÃO a reposta deve ser de falha
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    # E ENTÃO a registration não deve ser duplicada.
    assert EventRegistration.objects.count() == 1


@pytest.mark.django_db
def test_register_unauthorized(api_client, event_factory):
    # DADO nenhum usuário autenticado.
    # E DADO um evento.
    event = event_factory(slug="event-a", owners=[])

    # QUANDO a API é chamada para registrar o usuário no evento.
    resp = api_client.post(
        reverse("event-registration-list"), {"event_slug": event.slug}
    )

    # ENTÃO a reposta deve ser de falta de permissões
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO a registration não deve ser criada.
    assert EventRegistration.objects.count() == 0


@pytest.mark.django_db
def test_register_out_of_registration_period(
    api_client, user_factory, event_factory, freezer, parse_to_aware_datetime
):
    # DADO um usuário autenticado, e um evento.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event = event_factory(
        slug="event-a",
        owners=[],
        starts_on=parse_to_aware_datetime("2020-01-01"),
        ends_on=parse_to_aware_datetime("2020-02-02"),
    )
    # E DADO que já passou o tempo de inscrição.
    freezer.move_to(parse_to_aware_datetime("2020-03-03"))

    # QUANDO a API é chamada para registrar o usuário no evento.
    resp = api_client.post(
        reverse("event-registration-list"), {"event_slug": event.slug}
    )
    # ENTÃO a reposta de falha deve conter o erro no campo event.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["event_slug"]) != 0
    # E ENTÃO a registration não deve ser criada.
    assert EventRegistration.objects.count() == 0


@pytest.mark.django_db
def test_unregister_valid(api_client, user_factory, event_factory):
    # DADO um usuário autenticado, um evento no qual ele está registrado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    registration = EventRegistration.objects.create(event=event, user=user)

    # QUANDO a API é chamada para remover o registro do usuário no evento.
    resp = api_client.delete(
        reverse("event-registration-detail", args=[registration.id]),
    )

    # ENTÃO a reposta deve ser de sucesso
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    # E ENTÃO a registration deve ser removida.
    assert EventRegistration.objects.count() == 0


@pytest.mark.django_db
def test_unregister_other_user_unauthorized(api_client, user_factory, event_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    # E DADO um outro usuário alvo, e um evento no qual ele está registrado.
    target_user = user_factory(name="target", permissions=[])
    event = event_factory(slug="event-a", owners=[])
    registration = EventRegistration.objects.create(event=event, user=target_user)

    # QUANDO a API é chamada para remover o registro do usuário alvo no evento.
    resp = api_client.delete(
        reverse("event-registration-detail", args=[registration.id]),
    )

    # ENTÃO a reposta deve ser de falta de permissões
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO a registration deve permanecer inalterada.
    assert EventRegistration.objects.count() == 1


@pytest.mark.django_db
def test_list_registrations_for_user_and_event(api_client, user_factory, event_factory):
    # DADO um usuário autenticado, e dois eventos.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event_a = event_factory(slug="event-a", owners=[])
    event_b = event_factory(slug="event-b", owners=[])
    # E DADO duas inscrições do usuário, uma em cada evento.
    EventRegistration.objects.create(event=event_a, user=user)
    EventRegistration.objects.create(event=event_b, user=user)

    # QUANDO a API é chamada para listar as inscrições do usuário.
    resp = api_client.get(
        "{}?user_public_id={}".format(
            reverse("event-registration-list"), user.public_id
        )
    )

    # ENTÃO as inscrições do usuário serão retornadas
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data) == 2

    # E QUANDO a API é chamada para listar as inscrições do usuário no evento B.
    resp = api_client.get(
        "{}?user_public_id={}&event_slug={}".format(
            reverse("event-registration-list"), user.public_id, event_b.slug
        )
    )

    # ENTÃO a inscrição do usuário no evento será retornada.
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data) == 1


@pytest.mark.django_db
def test_list_registrations_for_user_unauthorized(
    api_client, user_factory, event_factory
):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    # E DADO um outro usuário alvo, e um evento no qual ele está registrado.
    target_user = user_factory(name="target", permissions=[])
    event = event_factory(slug="event-a", owners=[])
    EventRegistration.objects.create(event=event, user=target_user)

    # QUANDO a API é chamada para listar as inscrições do usuário alvo.
    resp = api_client.get(
        "{}?user_public_id={}".format(
            reverse("event-registration-list"), target_user.public_id
        )
    )

    # ENTÃO a reposta deve ser de falta de permissões
    assert resp.status_code == status.HTTP_403_FORBIDDEN
