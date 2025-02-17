from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from eventos2.core.models import Activity, ActivityRegistration, EventRegistration


@pytest.mark.django_db
def test_create_valid(api_client, user_factory, event_factory):
    # DADO um usuário autenticado e um evento pertencente a ele.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(
        slug="event-a",
        owners=[user],
        starts_on=timezone.now(),
        ends_on=timezone.now() + timedelta(days=1),
    )

    # E DADO dados de activity válidos.
    # QUANDO a API é chamada.
    resp = api_client.post(
        reverse("activity-list"),
        {
            "event_slug": event.slug,
            "name": "Activity A",
            "starts_on": event.starts_on,
            "ends_on": event.ends_on,
        },
    )

    # ENTÃO a resposta de sucesso deve conter os dados da activity,
    # incluindo o ID criado.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["name"] == "Activity A"
    assert resp.data["is_open"] is True

    # E ENTÃO a activity deve existir.
    assert Activity.objects.get(id=resp.data["id"]).name == "Activity A"


@pytest.mark.django_db
def test_create_invalid_date_order(api_client, user_factory, event_factory):
    # DADO um usuário autenticado e um evento pertencente a ele.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[user])

    # E DADO dados de activity inválidos (data de término antes do inicio).
    # QUANDO a API é chamada.
    resp = api_client.post(
        reverse("activity-list"),
        {
            "event_slug": event.slug,
            "name": "Activity A",
            "starts_on": timezone.now(),
            "ends_on": timezone.now() - timedelta(days=1),
        },
    )

    # ENTÃO a resposta deve ser de falha.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    # E ENTÃO a activity não deve ser criada.
    assert Activity.objects.count() == 0


@pytest.mark.django_db
def test_create_invalid_date_outside_of_event(
    api_client, user_factory, event_factory, parse_to_aware_datetime
):
    # DADO um usuário autenticado e um evento pertencente a ele.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(
        slug="event-a",
        owners=[user],
        starts_on=parse_to_aware_datetime("2020-02-02"),
        ends_on=parse_to_aware_datetime("2020-03-03"),
    )

    # E DADO dados de activity inválidos (datas fora dos limites do evento).
    # QUANDO a API é chamada.
    resp = api_client.post(
        reverse("activity-list"),
        {
            "event_slug": event.slug,
            "name": "Activity A",
            "starts_on": parse_to_aware_datetime("2020-01-01"),
            "ends_on": parse_to_aware_datetime("2020-04-04"),
        },
    )

    # ENTÃO a resposta deve ser de falha.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    # E ENTÃO a activity não deve ser criada.
    assert Activity.objects.count() == 0


@pytest.mark.django_db
def test_create_unauthorized(api_client, user_factory, event_factory):
    # DADO um usuário e um evento não pertencente a ele.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])

    # QUANDO a API é chamada para criar uma activity.
    resp = api_client.post(
        reverse("activity-list"),
        {
            "event_slug": event.slug,
            "name": "Activity A",
            "starts_on": timezone.now(),
            "ends_on": timezone.now(),
        },
    )

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # E ENTÃO a activity não deve ser criada.
    assert Activity.objects.count() == 0


@pytest.mark.django_db
def test_retrieve_valid(api_client, user_factory, event_factory, activity_factory):
    # DADO um usuário, um evento fechado, e uma activity fechada.
    user = user_factory(name="user", permissions=["core.view_activities_for_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(
        slug="event-a",
        owners=[],
        starts_on=timezone.now() + timedelta(days=-20),
        ends_on=timezone.now() + timedelta(days=-10),
    )
    activity = activity_factory(
        event=event,
        name="Activity A",
        owners=[],
        starts_on=event.starts_on,
        ends_on=event.ends_on,
    )

    # QUANDO a API é chamada para obter a activity.
    resp = api_client.get(reverse("activity-detail", args=[activity.id]))

    # ENTÃO a resposta de sucesso deve conter os dados da activity.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["name"] == activity.name
    assert resp.data["is_open"] is False


@pytest.mark.django_db
def test_retrieve_unauthorized(api_client, event_factory, activity_factory):
    # DADO nenhum usuário autenticado
    # E DADO um evento.
    event = event_factory(slug="event-a", owners=[])

    # E DADO um activity existente no evento.
    activity = activity_factory(event=event, name="Activity A", owners=[])

    # QUANDO a API é chamada para obter a activity.
    resp = api_client.get(reverse("activity-detail", args=[activity.id]))

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_valid(api_client, user_factory, event_factory, activity_factory):
    # DADO um usuário autenticado, e um evento pertencente a ele.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[user])

    # E DADO uma activity existente no evento.
    activity = activity_factory(
        event=event,
        name="Activity A",
        owners=[],
        starts_on=event.starts_on,
        ends_on=event.ends_on,
    )

    # E DADO dados de activity válidos.
    # QUANDO a API é chamada.
    resp = api_client.put(
        reverse("activity-detail", args=[activity.id]),
        {
            "name": "{} modified!".format(activity.name),
            "starts_on": activity.starts_on,
            "ends_on": activity.ends_on,
        },
    )

    # ENTÃO a reposta de sucesso deve conter a activity modificada.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["name"] == "{} modified!".format(activity.name)

    # E ENTÃO a activity deve ser modificada.
    assert Activity.objects.get(pk=activity.id).name == "{} modified!".format(
        activity.name
    )
    assert Activity.objects.count() == 1


@pytest.mark.django_db
def test_update_unauthorized(api_client, user_factory, event_factory, activity_factory):
    # DADO um usuário autenticado, e um evento não pertencente a ele.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])

    # E DADO uma activity existente no evento.
    activity = activity_factory(event=event, name="Activity A", owners=[])

    # QUANDO a API é chamada para editar a activity.
    resp = api_client.put(
        reverse("activity-detail", args=[activity.id]),
        {
            "name": activity.name + " modified",
            "starts_on": activity.starts_on,
            "ends_on": activity.ends_on,
        },
    )

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # E ENTÃO a activity não deve ser modificada.
    assert Activity.objects.get(pk=activity.id).name == activity.name


@pytest.mark.django_db
def test_delete_valid(api_client, user_factory, event_factory, activity_factory):
    # DADO um usuário autenticado, e um evento pertencente a ele.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[user])

    # E DADO uma activity.
    activity = activity_factory(event=event, name="Activity A", owners=[])

    # QUANDO a API é chamada para deletar a activity.
    delete_resp = api_client.delete(reverse("activity-detail", args=[activity.id]))

    # ENTÃO a deleção deverá ter sucesso.
    assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

    # E ENTÃO a activity não existirá.
    assert Activity.available_objects.count() == 0

    # E QUANDO a API é chamada para obter a activity deletada.
    retrieve_resp = api_client.get(reverse("activity-detail", args=[activity.id]))

    # ENTÃO a activity não será encontrada.
    assert retrieve_resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_unauthorized(api_client, user_factory, event_factory, activity_factory):
    # DADO um usuário autenticado, e um evento não pertencente a ele.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])

    # E DADO uma activity existente no evento.
    activity = activity_factory(event=event, name="Activity A", owners=[])

    # QUANDO a API é chamada para deletar a activity.
    resp = api_client.delete(reverse("activity-detail", args=[activity.id]))

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # E ENTÃO a activity não deve ser deletada.
    assert Activity.objects.count() == 1


@pytest.mark.django_db
def test_list_registrations(api_client, user_factory, event_factory, activity_factory):
    # DADO um usuário autenticado, um evento não pertencente ao usuário,
    # e uma activity no evento, pertencendo ao usuário.
    user = user_factory(
        name="user", permissions=["core.view_registrations_for_activity"]
    )
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    activity = activity_factory(event=event, name="Activity A", owners=[user])
    # E DADO uma inscrição de outro usuário na activity.
    other_user = user_factory(name="other_user", permissions=[])
    ActivityRegistration.objects.create(
        activity=activity,
        event_registration=EventRegistration.objects.create(
            event=event, user=other_user
        ),
    )

    # QUANDO a API é chamada para listar as inscrições da activity.
    resp = api_client.get(reverse("activity-list-registrations", args=[activity.id]))

    # ENTÃO as inscrições serão retornadas
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data) == 1
    assert resp.data[0]["user"]["email"] == other_user.email


@pytest.mark.django_db
def test_list_registrations_unauthorized(
    api_client, user_factory, event_factory, activity_factory
):
    # DADO um usuário autenticado, um evento não pertencente ao usuário,
    # e uma activity no evento, também não pertencendo ao usuário.
    user = user_factory(
        name="user", permissions=["core.view_registrations_for_activity"]
    )
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    activity = activity_factory(event=event, name="Activity A", owners=[])
    # E DADO uma inscrição de outro usuário na activity.
    other_user = user_factory(name="other_user", permissions=[])
    ActivityRegistration.objects.create(
        activity=activity,
        event_registration=EventRegistration.objects.create(
            event=event, user=other_user
        ),
    )

    # QUANDO a API é chamada para listar as inscrições da activity.
    resp = api_client.get(reverse("activity-list-registrations", args=[activity.id]))

    # ENTÃO a resposta deve ser de falta de permissões
    assert resp.status_code == status.HTTP_403_FORBIDDEN
