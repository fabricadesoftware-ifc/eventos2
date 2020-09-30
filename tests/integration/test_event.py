from datetime import timedelta

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
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["slug"] == "event-a"
    # E ENTÃO o evento deve existir.
    assert Event.objects.get(slug=resp.data["slug"]).name == "Event A"


@pytest.mark.django_db
def test_create_invalid_dates(api_client, user_factory, event_factory):
    # DADO um usuário autenticado com as permissões adequadas.
    user = user_factory(name="user", permissions=["core.add_event"])
    api_client.force_authenticate(user=user)

    # E DADO dados de evento inválidos (data de término antes do inicio).
    # QUANDO a API é chamada.
    resp = api_client.post(
        reverse("event-list"),
        {
            "slug": "event-a",
            "name": "Event A",
            "starts_on": timezone.now(),
            "ends_on": timezone.now() - timedelta(days=1),
        },
    )

    # ENTÃO a resposta deve ser de falha.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    # E ENTÃO o evento não deve ser criado.
    assert Event.objects.count() == 0


@pytest.mark.django_db
def test_create_duplicate_slug(api_client, user_factory, event_factory):
    # DADO um usuário autenticado com as permissões adequadas.
    user = user_factory(name="user", permissions=["core.add_event"])
    api_client.force_authenticate(user=user)
    # E DADO um evento
    existing_event = event_factory(slug="event-a", owners=[])

    # QUANDO a API é chamada para criar um evento com o mesmo slug.
    resp = api_client.post(
        reverse("event-list"),
        {
            "slug": existing_event.slug,
            "name": "Event B",
            "starts_on": timezone.now(),
            "ends_on": timezone.now(),
        },
    )

    # ENTÃO a resposta de falha deve conter o erro no campo slug.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["slug"]) != 0
    # E ENTÃO o evento não deve ser criado.
    assert Event.objects.count() == 1


@pytest.mark.django_db
def test_create_unauthorized(api_client, user_factory):
    # DADO um usuário sem as permissões adequadas.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # QUANDO a API é chamada para criar um evento.
    resp = api_client.post(
        reverse("event-list"),
        {
            "slug": "event-a",
            "name": "Event A",
            "starts_on": timezone.now(),
            "ends_on": timezone.now(),
        },
    )

    # ENTÃO a resposta deve ser de falta de permissão.
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO o evento não deve ser criado.
    assert Event.objects.count() == 0


@pytest.mark.django_db
def test_retrieve_valid(api_client, user_factory, event_factory):
    # DADO um evento.
    event = event_factory(slug="event-a", owners=[])

    # QUANDO a API é chamada para obter o evento.
    resp = api_client.get(reverse("event-detail", args=[event.slug]))

    # ENTÃO a resposta de sucesso deve conter os dados do evento.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["slug"] == event.slug


@pytest.mark.django_db
def test_update_valid(api_client, user_factory, event_factory):
    # DADO um usuário autenticado, e um evento pertencente a ele.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[user])

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
    assert resp.data["name"] == event.name
    assert resp.data["slug"] == "{} modified!".format(event.slug)
    # E ENTÃO o evento deve ser modificado.
    assert Event.objects.get(pk=event.id).slug == "{} modified!".format(event.slug)
    assert Event.objects.count() == 1


@pytest.mark.django_db
def test_update_duplicate_slug(api_client, user_factory, event_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    # E DADO dois eventos, um pertencente ao usuário.
    event_a = event_factory(slug="event-a", owners=[])
    event_b = event_factory(slug="event-b", owners=[user])

    # E DADO dados de evento inválidos (valor de slug utilizado por outro evento).
    # QUANDO a API é chamada.
    resp = api_client.put(
        reverse("event-detail", args=[event_b.slug]),
        {
            "slug": event_a.slug,
            "name": event_b.name,
            "starts_on": event_b.starts_on,
            "ends_on": event_b.ends_on,
        },
    )

    # ENTÃO a resposta de falha deve conter o erro no campo slug.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["slug"]) != 0
    # E ENTÃO o evento não deve ser modificado.
    assert Event.objects.get(pk=event_b.id).slug == event_b.slug


@pytest.mark.django_db
def test_update_unauthorized(api_client, user_factory, event_factory):
    # DADO um usuário autenticado, e um evento não pertencente a ele.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])

    # QUANDO a API é chamada.
    resp = api_client.put(
        reverse("event-detail", args=[event.slug]),
        {
            "slug": event.slug,
            "name": event.name + " modified",
            "starts_on": event.starts_on,
            "ends_on": event.ends_on,
        },
    )

    # ENTÃO a resposta deve ser de falta de permissão.
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO o evento não deve ser modificado.
    assert Event.objects.get(pk=event.id).name == event.name


@pytest.mark.django_db
def test_delete_valid(api_client, user_factory, event_factory):
    # DADO um usuário autenticado, e um evento pertencente a ele.
    user = user_factory(name="user", permissions=["core.delete_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[user])

    # QUANDO a API é chamada para deletar o evento.
    delete_resp = api_client.delete(reverse("event-detail", args=[event.slug]))

    # ENTÃO a deleção deverá ter sucesso.
    assert delete_resp.status_code == status.HTTP_204_NO_CONTENT
    # E ENTÃO o evento não existirá.
    assert Event.available_objects.count() == 0

    # E QUANDO a API é chamada para obter o evento deletado.
    retrieve_resp = api_client.get(reverse("event-detail", args=[event.slug]))

    # ENTÃO o evento não será encontrado.
    assert retrieve_resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_unauthorized(api_client, user_factory, event_factory):
    # DADO um usuário autenticado, e um evento não pertencente a ele.
    user = user_factory(name="user", permissions=["core.delete_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])

    # QUANDO a API é chamada para deletar o evento.
    resp = api_client.delete(reverse("event-detail", args=[event.slug]))

    # ENTÃO a resposta deve ser de falta de permissão.
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO o evento não será deletado.
    assert Event.available_objects.count() == 1


@pytest.mark.django_db
def test_list_registrations(api_client, user_factory, event_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=["core.view_registrations_for_event"])
    api_client.force_authenticate(user=user)
    # E DADO dois eventos, um pertencente ao usuário.
    event_a = event_factory(slug="event-a", owners=[])
    event_b = event_factory(slug="event-b", owners=[user])
    # E DADO uma inscrição em cada evento.
    registration_a = EventRegistration.objects.create(event=event_a, user=user)
    EventRegistration.objects.create(event=event_b, user=user)

    # QUANDO a API é chamada para listar as inscrições do evento pertencente ao usuário.
    resp = api_client.get(reverse("event-list-registrations", args=[event_b.slug]))

    # ENTÃO apenas as inscrições do evento A serão retornadas
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data) == 1
    assert resp.data[0]["user"]["email"] == registration_a.user.email


@pytest.mark.django_db
def test_list_registrations_unauthorized(api_client, user_factory, event_factory):
    # DADO um usuário autenticado, e um evento não pertencente a ele.
    user = user_factory(name="user", permissions=["core.view_registrations_for_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])

    # QUANDO a API é chamada para listar as inscrições do evento.
    resp = api_client.get(reverse("event-list-registrations", args=[event.slug]))

    # ENTÃO a resposta deve ser de falta de permissão.
    assert resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_list_activities(api_client, user_factory, event_factory, activity_factory):
    # DADO um usuário autenticado, um evento pertencente a ele,
    # e uma atividade no evento.
    user = user_factory(name="user", permissions=["core.view_activities_for_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[user])
    activity_a = activity_factory(event=event, name="Activity A", owners=[])

    # QUANDO a API é chamada para listar as activities do evento.
    resp = api_client.get(reverse("event-list-activities", args=[event.slug]))

    # ENTÃO as activities serão retornadas
    assert resp.status_code == status.HTTP_200_OK

    assert len(resp.data) == 1
    assert resp.data[0]["name"] == activity_a.name


@pytest.mark.django_db
def test_list_tracks(api_client, user_factory, event_factory, track_factory):
    # DADO um usuário autenticado, um evento pertencente a ele, e um track no evento.
    user = user_factory(name="user", permissions=["core.view_tracks_for_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[user])
    track_a = track_factory(event=event, name="Track A")

    # QUANDO a API é chamada para listar os tracks do evento.
    resp = api_client.get(reverse("event-list-tracks", args=[event.slug]))

    # ENTÃO os tracks serão retornados
    assert resp.status_code == status.HTTP_200_OK

    assert len(resp.data) == 1
    assert resp.data[0]["name"] == track_a.name
