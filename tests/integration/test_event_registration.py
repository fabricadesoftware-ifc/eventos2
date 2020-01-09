import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from eventos2.core.models import Event, EventRegistration, EventRegistrationType


@pytest.mark.django_db
def test_register_self_valid(api_client, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento com registration type existente.
    event = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )
    registration_type = EventRegistrationType.objects.create(
        name="Registration type A", event=event
    )

    # QUANDO a API é chamada para registrar o usuário no evento.
    resp = api_client.post(
        reverse("event-registration-list"),
        {"registration_type": registration_type.id, "user": user.id},
    )

    # ENTÃO a reposta deve ser de sucesso
    assert resp.status_code == status.HTTP_201_CREATED

    # E ENTÃO a registration deve ser criado.
    assert EventRegistration.objects.count() == 1


@pytest.mark.django_db
def test_register_self_duplicate(api_client, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento com registration type existente,
    # no qual o usuário já está registrado.
    event = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )
    registration_type = EventRegistrationType.objects.create(
        name="Registration type A", event=event
    )
    EventRegistration.objects.create(registration_type=registration_type, user=user)

    # QUANDO a API é chamada para registrar o usuário no evento novamente.
    resp = api_client.post(
        reverse("event-registration-list"),
        {"registration_type": registration_type.id, "user": user.id},
    )

    # ENTÃO a reposta deve ser de falha
    assert resp.status_code == status.HTTP_409_CONFLICT

    # E ENTÃO a registration não deve ser duplicada.
    assert EventRegistration.objects.count() == 1


@pytest.mark.django_db
def test_register_other_user_unauthorized(api_client, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um outro usuário alvo
    target_user = user_factory(name="target", permissions=[])

    # E DADO um evento com registration type existente.
    event = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )
    registration_type = EventRegistrationType.objects.create(
        name="Registration type A", event=event
    )

    # QUANDO a API é chamada para registrar o usuário alvo no evento.
    resp = api_client.post(
        reverse("event-registration-list"),
        {"registration_type": registration_type.id, "user": target_user.id},
    )

    # ENTÃO a reposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # E ENTÃO a registration não deve ser criado.
    assert EventRegistration.objects.count() == 0


@pytest.mark.django_db
def test_unregister_self_valid(api_client, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento com registration type existente,
    # no qual o usuário já está registrado.
    event = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )
    registration_type = EventRegistrationType.objects.create(
        name="Registration type A", event=event
    )
    registration = EventRegistration.objects.create(
        registration_type=registration_type, user=user
    )

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

    # E DADO um evento com registration type existente,
    # no qual o usuário alvo já está registrado.
    event = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )
    registration_type = EventRegistrationType.objects.create(
        name="Registration type A", event=event
    )
    registration = EventRegistration.objects.create(
        registration_type=registration_type, user=target_user
    )

    # QUANDO a API é chamada para remover o registro do usuário alvo no evento.
    resp = api_client.delete(
        reverse("event-registration-detail", args=[registration.id]),
    )

    # ENTÃO a reposta deve ser de falta de permissões
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # E ENTÃO a registration deve permanecer inalterada no banco.
    assert EventRegistration.objects.count() == 1
