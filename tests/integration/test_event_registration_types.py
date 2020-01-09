import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from eventos2.core.models import Event, EventRegistration, EventRegistrationType


@pytest.mark.django_db
def test_create_valid(api_client, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, pertencente ao usuário.
    event = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )
    event.owners.add(user)

    # QUANDO a API é chamda para criar um registration type no evento.
    resp = api_client.post(
        reverse("event-registration-type-list"),
        {"name": "Registration type A", "event": event.id},
    )

    # ENTÃO a resposta de sucesso deve conter os dados do registration type,
    # incluindo o ID criado.
    assert resp.status_code == status.HTTP_201_CREATED
    assert type(resp.data["id"]) is int
    assert resp.data["name"] == "Registration type A"

    # E ENTÃO o registration type deve existir no banco.
    assert (
        EventRegistrationType.objects.get(pk=resp.data["id"]).name
        == "Registration type A"
    )


@pytest.mark.django_db
def test_create_unauthorized(api_client, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, não pertencente ao usuário.
    event = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )

    # QUANDO a API é chamda tentando criar um registration type no evento.
    resp = api_client.post(
        reverse("event-registration-type-list"),
        {"name": "Registration type A", "event": event.id},
    )

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # E ENTÃO o registration type não deve ser criado.
    assert EventRegistrationType.objects.exists() is False


@pytest.mark.django_db
def test_update_valid(api_client, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, pertencente ao usuário.
    event = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )
    event.owners.add(user)

    # E DADO um registration type existente para o evento.
    registration_type = EventRegistrationType.objects.create(
        name="Registration type A", event=event
    )

    # QUANDO a API é chamda para alterar o registration type.
    resp = api_client.put(
        reverse("event-registration-type-detail", args=[registration_type.id]),
        {"name": "{} modified!".format(registration_type.name)},
    )

    # ENTÃO a resposta de sucesso deve conter o registration type modificado.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["name"] == "{} modified!".format(registration_type.name)

    # E ENTÃO o registration type deve ser modificado no banco.
    assert EventRegistrationType.objects.get(
        pk=registration_type.id
    ).name == "{} modified!".format(registration_type.name)


@pytest.mark.django_db
def test_update_unauthorized(api_client, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, não pertencente ao usuário.
    event = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )

    # E DADO um registration type existente para o evento.
    registration_type = EventRegistrationType.objects.create(
        name="Registration type A", event=event
    )

    # QUANDO a API é chamda tentando alterar o registration type.
    resp = api_client.put(
        reverse("event-registration-type-detail", args=[registration_type.id]),
        {"name": "{} modified!".format(registration_type.name)},
    )

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # E ENTÃO o registration type deve permanecer inalterado no banco.
    assert (
        EventRegistrationType.objects.get(pk=registration_type.id).name
        == registration_type.name
    )


@pytest.mark.django_db
def test_delete_valid(api_client, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, pertencente ao usuário.
    event = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )
    event.owners.add(user)

    # E DADO um registration type existente para o evento.
    registration_type = EventRegistrationType.objects.create(
        name="Registration type A", event=event
    )

    # QUANDO a API é chamda para deletar o registration type.
    resp = api_client.delete(
        reverse("event-registration-type-detail", args=[registration_type.id]),
    )

    # ENTÃO a resposta deve ser de sucesso.
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    # E ENTÃO o registration type deve deixar de existir no banco.
    assert (
        EventRegistrationType.objects.filter(pk=registration_type.id).exists() is False
    )


@pytest.mark.django_db
def test_delete_unauthorized(api_client, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, não pertencente ao usuário.
    event = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )

    # E DADO um registration type existente para o evento.
    registration_type = EventRegistrationType.objects.create(
        name="Registration type A", event=event
    )

    # QUANDO a API é chamda tentando deletar o registration type.
    resp = api_client.delete(
        reverse("event-registration-type-detail", args=[registration_type.id]),
    )

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # E ENTÃO o registration type deve permanecer inalterado no banco.
    assert (
        EventRegistrationType.objects.get(pk=registration_type.id).name
        == registration_type.name
    )


@pytest.mark.django_db
def test_list_registrations(api_client, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, pertencente ao usuário.
    event = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )
    event.owners.add(user)

    # E DADO um registration type existente para o evento.
    registration_type = EventRegistrationType.objects.create(
        name="Registration type A", event=event
    )

    # E DADO inscrições no registration type.
    registration_a = EventRegistration.objects.create(
        registration_type=registration_type, user=user
    )

    # QUANDO a API é chamada para listar as inscrições do registration type.
    resp = api_client.get(
        reverse(
            "event-registration-type-list-registrations", args=[registration_type.id]
        ),
    )

    # ENTÃO a resposta deve ser de sucesso.
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data) == 1
    assert resp.data[0]["user"]["email"] == registration_a.user.email
