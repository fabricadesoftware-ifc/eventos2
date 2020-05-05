import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from eventos2.core.models import Activity


@pytest.mark.django_db
def test_create_valid(api_client, user_factory, event_factory):
    # DADO um usuário autenticado com as permissões adequadas.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento.
    event = event_factory(slug="event-a", owners=[user])

    # E DADO dados de activity válidos.
    # QUANDO a API é chamada.
    resp = api_client.post(
        reverse("activity-list"),
        {
            "event": event.id,
            "slug": "activity-a",
            "name": "Activity A",
            "starts_on": timezone.now(),
            "ends_on": timezone.now(),
        },
    )

    # ENTÃO a resposta de sucesso deve conter os dados da activity,
    # incluindo o ID criado.
    assert resp.status_code == status.HTTP_201_CREATED
    assert type(resp.data["id"]) is int
    assert resp.data["slug"] == "activity-a"

    # E ENTÃO a activity deve existir no banco.
    assert Activity.objects.get(pk=resp.data["id"]).slug == "activity-a"


@pytest.mark.django_db
def test_create_unauthorized(api_client, user_factory, event_factory):
    # DADO um usuário.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)

    # E DADO um evento.
    event = event_factory(slug="event-a", owners=[])

    # E DADO dados de activity inválidos (evento não pertence ao usuário).
    # QUANDO a API é chamada.
    resp = api_client.post(
        reverse("activity-list"),
        {
            "event": event.id,
            "slug": "activity-a",
            "name": "Activity A",
            "starts_on": timezone.now(),
            "ends_on": timezone.now(),
        },
    )

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # E ENTÃO a activity não deve ser criada no banco.
    assert Activity.objects.count() == 0


@pytest.mark.django_db
def test_retrieve_valid(api_client, user_factory, event_factory):
    # DADO um usuário.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento.
    event = event_factory(slug="event-a", owners=[])

    # E DADO um activity existente no banco.
    activity = Activity.objects.create(
        event=event,
        slug="activity-a",
        name="Activity A",
        starts_on=timezone.now(),
        ends_on=timezone.now(),
    )

    # QUANDO a API é chamada para obter a activity.
    resp = api_client.get(reverse("activity-detail", args=[activity.slug]))

    # ENTÃO a resposta de sucesso deve conter os dados da activity.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["slug"] == activity.slug


@pytest.mark.django_db
def test_retrieve_invalid(api_client):
    # DADO nenhuma activity no banco.

    # QUANDO a API é chamada para obter um activity inexistente.
    resp = api_client.get(reverse("activity-detail", args=["slug-inexistente"]))

    # ENTÃO a resposta deve ser de falha
    assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_valid(api_client, user_factory, event_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, pertencente ao usuário.
    event = event_factory(slug="event-a", owners=[user])

    # E DADO uma activity existente no banco.
    activity = Activity.objects.create(
        event=event,
        name="Activity A",
        slug="activity-a",
        starts_on=timezone.now(),
        ends_on=timezone.now(),
    )

    # E DADO dados de activity válidos.
    # QUANDO a API é chamada.
    resp = api_client.put(
        reverse("activity-detail", args=[activity.slug]),
        {
            "slug": "{} modified!".format(activity.slug),
            "name": activity.name,
            "starts_on": activity.starts_on,
            "ends_on": activity.ends_on,
        },
    )

    # ENTÃO a reposta de sucesso deve conter a activity modificada.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["id"] == activity.id
    assert resp.data["slug"] == "{} modified!".format(activity.slug)

    # E ENTÃO a activity deve ser modificada no banco.
    assert Activity.objects.get(pk=activity.id).slug == "{} modified!".format(
        activity.slug
    )
    assert Activity.objects.count() == 1


@pytest.mark.django_db
def test_update_invalid(api_client, user_factory, event_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, pertencente ao usuário.
    event = event_factory(slug="event-a", owners=[user])

    # E DADO uma activity existente no banco.
    activity = Activity.objects.create(
        event=event,
        slug="activity-a",
        name="Activity A",
        starts_on=timezone.now(),
        ends_on=timezone.now(),
    )

    # E DADO dados de activity inválidos (valor de slug é nulo).
    # QUANDO a API é chamada.
    resp = api_client.put(
        reverse("activity-detail", args=[activity.slug]),
        {
            "slug": None,
            "name": activity.name,
            "starts_on": activity.starts_on,
            "ends_on": activity.ends_on,
        },
    )

    # ENTÃO a resposta de falha deve conter os erros de cada campo.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["slug"]) != 0

    # E ENTÃO a activity não deve ser modificada no banco.
    assert Activity.objects.get(pk=activity.id).slug == activity.slug


@pytest.mark.django_db
def test_delete_valid(api_client, user_factory, event_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, pertencente ao usuário.
    event = event_factory(slug="event-a", owners=[user])

    # E DADO uma activity existente no banco.
    activity = Activity.objects.create(
        event=event,
        slug="activity-a",
        name="Activity A",
        starts_on=timezone.now(),
        ends_on=timezone.now(),
    )

    # QUANDO a API é chamada para deletar a activity.
    delete_resp = api_client.delete(reverse("activity-detail", args=[activity.slug]))

    # ENTÃO a deleção deverá ter sucesso.
    assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

    # E ENTÃO a activity não existirá no banco.
    assert Activity.available_objects.count() == 0

    # E QUANDO a API é chamada para obter a activity deletado.
    retrieve_resp = api_client.get(reverse("activity-detail", args=[activity.slug]))

    # ENTÃO a activity não será encontrado.
    assert retrieve_resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_invalid(api_client, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # QUANDO a API é chamada para deletar um activity que não existe.
    resp = api_client.delete(reverse("activity-detail", args=["slug-inexistente"]))

    # ENTÃO a activity não será encontrado.
    assert resp.status_code == status.HTTP_404_NOT_FOUND
