import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from eventos2.core.models import Event, EventRegistration


@pytest.mark.django_db
def test_create_valid(api_client, user_factory):
    # DADO um usuário autenticado com as permissões adequadas.
    user = user_factory(name="user", permissions=["core.add_event"])
    api_client.force_authenticate(user=user)

    # E DADO dados de evento válidos.
    # QUANDO a API é chamada.
    resp = api_client.post(
        reverse("event-list"),
        {
            "slug": "event-a",
            "name": "Event A",
            "starts_on": timezone.now(),
            "ends_on": timezone.now(),
        },
    )

    # ENTÃO a resposta de sucesso deve conter os dados do evento,
    # incluindo o ID criado.
    assert resp.status_code == status.HTTP_201_CREATED
    assert type(resp.data["id"]) is int
    assert resp.data["slug"] == "event-a"

    # E ENTÃO o evento deve existir no banco.
    assert Event.objects.get(pk=resp.data["id"]).slug == "event-a"


@pytest.mark.django_db
def test_create_invalid(api_client, user_factory):
    # DADO um usuário autenticado com as permissões adequadas.
    user = user_factory(name="user", permissions=["core.add_event"])
    api_client.force_authenticate(user=user)

    # E DADO dados de evento inválidos (valor de slug é nulo).
    # QUANDO a API é chamada.
    resp = api_client.post(
        reverse("event-list"),
        {
            "slug": None,
            "name": "Event A",
            "starts_on": timezone.now(),
            "ends_on": timezone.now(),
        },
    )

    # ENTÃO a resposta de falha deve conter os erros de cada campo.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["slug"]) != 0

    # E ENTÃO o evento não deve ser criado no banco.
    assert Event.objects.count() == 0


@pytest.mark.django_db
def test_retrieve_valid(api_client, user_factory):
    # DADO um evento existente no banco.
    event = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )

    # QUANDO a API é chamada para obter o evento.
    resp = api_client.get(reverse("event-detail", args=[event.slug]))

    # ENTÃO a resposta de sucesso deve conter os dados do evento.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["slug"] == event.slug


@pytest.mark.django_db
def test_retrieve_invalid(api_client, user_factory):
    # DADO nenhum evento no banco.

    # QUANDO a API é chamada para obter um evento inexistente.
    resp = api_client.get(reverse("event-detail", args=["slug-inexistente"]))

    # ENTÃO a resposta deve ser de falha
    assert resp.status_code == status.HTTP_404_NOT_FOUND


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

    # E DADO dados de evento válidos.
    # QUANDO a API é chamada.
    resp = api_client.put(
        reverse("event-detail", args=[event.slug]),
        {
            "slug": "{} modified!".format(event.slug),
            "name": event.name,
            "starts_on": event.starts_on,
            "ends_on": event.ends_on,
        },
    )

    # ENTÃO a reposta de sucesso deve conter o evento modificado.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["id"] == event.id
    assert resp.data["slug"] == "{} modified!".format(event.slug)

    # E ENTÃO o evento deve ser modificado no banco.
    assert Event.objects.get(pk=event.id).slug == "{} modified!".format(event.slug)
    assert Event.objects.count() == 1


@pytest.mark.django_db
def test_update_invalid(api_client, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, pertencente ao usuário.
    event = Event.objects.create(
        slug="event-a", name="Event A", starts_on=timezone.now(), ends_on=timezone.now()
    )
    event.owners.add(user)

    # E DADO dados de evento inválidos (valor de slug é nulo).
    # QUANDO a API é chamada.
    resp = api_client.put(
        reverse("event-detail", args=[event.slug]),
        {
            "slug": None,
            "name": event.name,
            "starts_on": event.starts_on,
            "ends_on": event.ends_on,
        },
    )

    # ENTÃO a resposta de falha deve conter os erros de cada campo.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["slug"]) != 0

    # E ENTÃO o evento não deve ser modificado no banco.
    assert Event.objects.get(pk=event.id).slug == event.slug


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

    # QUANDO a API é chamada para deletar o evento.
    delete_resp = api_client.delete(reverse("event-detail", args=[event.slug]))

    # ENTÃO a deleção deverá ter sucesso.
    assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

    # E ENTÃO o evento não existirá no banco.
    assert Event.available_objects.count() == 0

    # E QUANDO a API é chamada para obter o evento deletado.
    retrieve_resp = api_client.get(reverse("event-detail", args=[event.slug]))

    # ENTÃO o evento não será encontrado.
    assert retrieve_resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_invalid(api_client, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # QUANDO a API é chamada para deletar um evento que não existe.
    resp = api_client.delete(reverse("event-detail", args=["slug-inexistente"]))

    # ENTÃO o evento não será encontrado.
    assert resp.status_code == status.HTTP_404_NOT_FOUND


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

    # E DADO inscrições no evento.
    registration_a = EventRegistration.objects.create(event=event, user=user)

    # QUANDO a API é chamada para listar as inscrições do evento.
    resp = api_client.get(reverse("event-list-registrations", args=[event.slug]))

    # ENTÃO as inscrições serão retornadas
    assert resp.status_code == status.HTTP_200_OK

    assert len(resp.data) == 1
    assert resp.data[0]["user"]["email"] == registration_a.user.email
