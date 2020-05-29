import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from eventos2.core.models import Activity


@pytest.mark.django_db
def test_create_valid(api_client, user_factory, event_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento pertencente ao usuário.
    event = event_factory(slug="event-a", owners=[user])

    # E DADO dados de activity válidos.
    # QUANDO a API é chamada.
    resp = api_client.post(
        reverse("activity-list"),
        {
            "event": event.slug,
            "slug": "activity-a",
            "name": "Activity A",
            "starts_on": timezone.now(),
            "ends_on": timezone.now(),
        },
    )

    # ENTÃO a resposta de sucesso deve conter os dados da activity,
    # incluindo o ID criado.
    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.data["slug"] == "activity-a"

    # E ENTÃO a activity deve existir no banco.
    assert Activity.objects.get(slug=resp.data["slug"]).name == "Activity A"


@pytest.mark.django_db
def test_create_unauthorized(api_client, user_factory, event_factory):
    # DADO um usuário.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)

    # E DADO um evento não pertencente ao usuário.
    event = event_factory(slug="event-a", owners=[])

    # QUANDO a API é chamada para criar uma activity.
    resp = api_client.post(
        reverse("activity-list"),
        {
            "event": event.slug,
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
def test_create_duplicate_slug(api_client, user_factory, event_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento pertencente ao usuário.
    event = event_factory(slug="event-a", owners=[user])

    # E DADO uma activity existente no evento.
    existing_activity = Activity.objects.create(
        event=event,
        slug="activity-a",
        name="Activity A",
        starts_on=timezone.now(),
        ends_on=timezone.now(),
    )

    # QUANDO a API é chamada para criar uma activity com o mesmo slug.
    resp = api_client.post(
        reverse("activity-list"),
        {
            "event": event.slug,
            "slug": existing_activity.slug,
            "name": "Activity A",
            "starts_on": timezone.now(),
            "ends_on": timezone.now(),
        },
    )

    # ENTÃO a resposta de falha deve conter o erro no campo slug.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["slug"]) != 0

    # E ENTÃO a activity não deve ser criada no banco.
    assert Activity.objects.count() == 1


@pytest.mark.django_db
def test_retrieve_valid(api_client, user_factory, event_factory):
    # DADO um usuário.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento.
    event = event_factory(slug="event-a", owners=[])

    # E DADO um activity existente no evento.
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
def test_retrieve_unauthorized(api_client, event_factory):
    # DADO nenhum usuário autenticado.

    # E DADO um evento.
    event = event_factory(slug="event-a", owners=[])

    # E DADO um activity existente no evento.
    activity = Activity.objects.create(
        event=event,
        slug="activity-a",
        name="Activity A",
        starts_on=timezone.now(),
        ends_on=timezone.now(),
    )

    # QUANDO a API é chamada para obter a activity.
    resp = api_client.get(reverse("activity-detail", args=[activity.slug]))

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_update_valid(api_client, user_factory, event_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, pertencente ao usuário.
    event = event_factory(slug="event-a", owners=[user])

    # E DADO uma activity existente no evento.
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
    assert resp.data["name"] == activity.name
    assert resp.data["slug"] == "{} modified!".format(activity.slug)

    # E ENTÃO a activity deve ser modificada no banco.
    assert Activity.objects.get(pk=activity.id).slug == "{} modified!".format(
        activity.slug
    )
    assert Activity.objects.count() == 1


@pytest.mark.django_db
def test_update_duplicate_slug(api_client, user_factory, event_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, pertencente ao usuário.
    event = event_factory(slug="event-a", owners=[user])

    # E DADO duas activities existentes no evento.
    activity_a = Activity.objects.create(
        event=event,
        slug="activity-a",
        name="Activity A",
        starts_on=timezone.now(),
        ends_on=timezone.now(),
    )
    activity_b = Activity.objects.create(
        event=event,
        slug="activity-b",
        name="Activity B",
        starts_on=timezone.now(),
        ends_on=timezone.now(),
    )

    # E DADO dados de activity inválidos (valor de slug utilizado pela activity A).
    # QUANDO a API é chamada.
    resp = api_client.put(
        reverse("activity-detail", args=[activity_b.slug]),
        {
            "slug": activity_a.slug,
            "name": activity_b.name,
            "starts_on": activity_b.starts_on,
            "ends_on": activity_b.ends_on,
        },
    )

    # ENTÃO a resposta de falha deve conter o erro no campo slug.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["slug"]) != 0

    # E ENTÃO a activity não deve ser modificada no banco.
    assert Activity.objects.get(pk=activity_b.id).slug == activity_b.slug


@pytest.mark.django_db
def test_update_unauthorized(api_client, user_factory, event_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, não pertencente ao usuário.
    event = event_factory(slug="event-a", owners=[])

    # E DADO uma activity existente no evento.
    activity = Activity.objects.create(
        event=event,
        name="Activity A",
        slug="activity-a",
        starts_on=timezone.now(),
        ends_on=timezone.now(),
    )

    # QUANDO a API é chamada para editar a activity.
    resp = api_client.put(
        reverse("activity-detail", args=[activity.slug]),
        {
            "slug": activity.slug,
            "name": activity.name + " modified",
            "starts_on": activity.starts_on,
            "ends_on": activity.ends_on,
        },
    )

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # E ENTÃO a activity não deve ser modificada no banco.
    assert Activity.objects.get(pk=activity.id).name == activity.name


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
def test_delete_unauthorized(api_client, user_factory, event_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, não pertencente ao usuário.
    event = event_factory(slug="event-a", owners=[])

    # E DADO uma activity existente no evento.
    activity = Activity.objects.create(
        event=event,
        slug="activity-a",
        name="Activity A",
        starts_on=timezone.now(),
        ends_on=timezone.now(),
    )

    # QUANDO a API é chamada para deletar a activity.
    resp = api_client.delete(reverse("activity-detail", args=[activity.slug]))

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # E ENTÃO a activity não deve ser deletada.
    assert Activity.objects.count() == 1
