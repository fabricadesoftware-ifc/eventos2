import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from eventos2.core.models import Event, EventRegistration


@pytest.mark.django_db
def test_register_valid(api_client, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento.
    event = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )

    # QUANDO a API é chamada para registrar o usuário no evento.
    resp = api_client.post(reverse("event-registration-list"), {"event": event.id})

    # ENTÃO a reposta deve ser de sucesso
    assert resp.status_code == status.HTTP_201_CREATED

    # E ENTÃO a registration deve ser criado.
    assert EventRegistration.objects.count() == 1
    assert EventRegistration.objects.first().user == user


@pytest.mark.django_db
def test_register_duplicate(api_client, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento no qual o usuário já está registrado.
    event = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )
    EventRegistration.objects.create(event=event, user=user)

    # QUANDO a API é chamada para registrar o usuário no evento novamente.
    resp = api_client.post(reverse("event-registration-list"), {"event": event.id})

    # ENTÃO a reposta deve ser de falha
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    # E ENTÃO a registration não deve ser duplicada.
    assert EventRegistration.objects.count() == 1


@pytest.mark.django_db
def test_register_unauthorized(api_client):
    # DADO nenhum usuário autenticado.

    # E DADO um evento.
    event = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )

    # QUANDO a API é chamada para registrar o usuário no evento.
    resp = api_client.post(reverse("event-registration-list"), {"event": event.id})

    # ENTÃO a reposta deve ser de falta de permissões
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # E ENTÃO a registration não deve ser criada.
    assert EventRegistration.objects.count() == 0


@pytest.mark.django_db
def test_unregister_valid(api_client, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento no qual o usuário já está registrado.
    event = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )
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
def test_unregister_other_user_unauthorized(api_client, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um outro usuário alvo
    target_user = user_factory(name="target", permissions=[])

    # E DADO um evento no qual o usuário alvo já está registrado.
    event = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )
    registration = EventRegistration.objects.create(event=event, user=target_user)

    # QUANDO a API é chamada para remover o registro do usuário alvo no evento.
    resp = api_client.delete(
        reverse("event-registration-detail", args=[registration.id]),
    )

    # ENTÃO a reposta deve ser de falta de permissões
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # E ENTÃO a registration deve permanecer inalterada no banco.
    assert EventRegistration.objects.count() == 1


@pytest.mark.django_db
def test_list_registrations_for_user_and_event(api_client, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO dois eventos existentes no banco.
    event_a = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )
    event_b = Event.objects.create(
        slug="event-b", name="Event B", starts_on=timezone.now(), ends_on=timezone.now()
    )

    # E DADO duas inscrições do usuário, uma em cada evento.
    EventRegistration.objects.create(event=event_a, user=user)
    EventRegistration.objects.create(event=event_b, user=user)

    # QUANDO a API é chamada para listar as inscrições do usuário.
    resp = api_client.get(
        "{}?user_id={}".format(reverse("event-registration-list"), user.id)
    )

    # ENTÃO as inscrições do usuário serão retornadas
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data) == 2

    # E QUANDO a API é chamada para listar as inscrições do usuário no evento B.
    resp = api_client.get(
        "{}?user_id={}&event_id={}".format(
            reverse("event-registration-list"), user.id, event_b.id
        )
    )

    # ENTÃO a inscrição do usuário no evento será retornada.
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data) == 1
