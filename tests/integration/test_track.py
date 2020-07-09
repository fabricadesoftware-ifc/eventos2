import pytest
from django.urls import reverse
from rest_framework import status

from eventos2.core.models import Track


@pytest.mark.django_db
def test_create_valid(api_client, user_factory, event_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento pertencente ao usuário.
    event = event_factory(slug="event-a", owners=[user])

    # E DADO dados de track válidos.
    # QUANDO a API é chamada.
    resp = api_client.post(
        reverse("track-list"),
        {"event": event.slug, "slug": "track-a", "name": "Track A"},
    )

    # ENTÃO a resposta de sucesso deve conter os dados do track.
    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.data["slug"] == "track-a"

    # E ENTÃO o track deve existir no banco.
    assert Track.objects.get(slug=resp.data["slug"]).name == "Track A"


@pytest.mark.django_db
def test_create_unauthorized(api_client, user_factory, event_factory):
    # DADO um usuário.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)

    # E DADO um evento não pertencente ao usuário.
    event = event_factory(slug="event-a", owners=[])

    # QUANDO a API é chamada para criar um track.
    resp = api_client.post(
        reverse("track-list"),
        {"event": event.slug, "slug": "track-a", "name": "Track A"},
    )

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # E ENTÃO o track não deve ser criado no banco.
    assert Track.objects.count() == 0


@pytest.mark.django_db
def test_create_duplicate_slug(api_client, user_factory, event_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento pertencente ao usuário.
    event = event_factory(slug="event-a", owners=[user])

    # E DADO um track existente no evento.
    existing_track = Track.objects.create(event=event, slug="track-a", name="Track A")

    # QUANDO a API é chamada para criar um track com o mesmo slug.
    resp = api_client.post(
        reverse("track-list"),
        {"event": event.slug, "slug": existing_track.slug, "name": "Track A"},
    )

    # ENTÃO a resposta de falha deve conter o erro no campo slug.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["slug"]) != 0

    # E ENTÃO o track não deve ser criado no banco.
    assert Track.objects.count() == 1


@pytest.mark.django_db
def test_retrieve_valid(api_client, user_factory, event_factory):
    # DADO um usuário.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento.
    event = event_factory(slug="event-a", owners=[])

    # E DADO um track existente no evento.
    track = Track.objects.create(event=event, slug="track-a")

    # QUANDO a API é chamada para obter o track.
    resp = api_client.get(reverse("track-detail", args=[track.slug]))

    # ENTÃO a resposta de sucesso deve conter os dados do track.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["slug"] == track.slug


@pytest.mark.django_db
def test_retrieve_unauthorized(api_client, event_factory):
    # DADO nenhum usuário autenticado.

    # E DADO um evento.
    event = event_factory(slug="event-a", owners=[])

    # E DADO um track existente no evento.
    track = Track.objects.create(event=event, slug="track-a", name="Track A")

    # QUANDO a API é chamada para obter o track.
    resp = api_client.get(reverse("track-detail", args=[track.slug]))

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_update_valid(api_client, user_factory, event_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, pertencente ao usuário.
    event = event_factory(slug="event-a", owners=[user])

    # E DADO um track existente no evento.
    track = Track.objects.create(event=event, name="Track A", slug="track-a")

    # E DADO dados de track válidos.
    # QUANDO a API é chamada.
    resp = api_client.put(
        reverse("track-detail", args=[track.slug]),
        {"slug": "{} modified!".format(track.slug), "name": track.name},
    )

    # ENTÃO a reposta de sucesso deve conter o track modificado.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["name"] == track.name
    assert resp.data["slug"] == "{} modified!".format(track.slug)

    # E ENTÃO o track deve ser modificado no banco.
    assert Track.objects.get(pk=track.id).slug == "{} modified!".format(track.slug)
    assert Track.objects.count() == 1


@pytest.mark.django_db
def test_update_duplicate_slug(api_client, user_factory, event_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, pertencente ao usuário.
    event = event_factory(slug="event-a", owners=[user])

    # E DADO dois tracks existentes no evento.
    track_a = Track.objects.create(event=event, slug="track-a", name="Track A",)
    track_b = Track.objects.create(event=event, slug="track-b", name="Track B",)

    # E DADO dados de track inválidos (valor de slug utilizado pelo track A).
    # QUANDO a API é chamada.
    resp = api_client.put(
        reverse("track-detail", args=[track_b.slug]),
        {"slug": track_a.slug, "name": track_b.name},
    )

    # ENTÃO a resposta de falha deve conter o erro no campo slug.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["slug"]) != 0

    # E ENTÃO o track não deve ser modificado no banco.
    assert Track.objects.get(pk=track_b.id).slug == track_b.slug


@pytest.mark.django_db
def test_update_unauthorized(api_client, user_factory, event_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, não pertencente ao usuário.
    event = event_factory(slug="event-a", owners=[])

    # E DADO um track existente no evento.
    track = Track.objects.create(event=event, name="Track A", slug="track-a")

    # QUANDO a API é chamada para editar o track.
    resp = api_client.put(
        reverse("track-detail", args=[track.slug]),
        {"slug": track.slug, "name": track.name + " modified"},
    )

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # E ENTÃO o track não deve ser modificado no banco.
    assert Track.objects.get(pk=track.id).name == track.name


@pytest.mark.django_db
def test_delete_valid(api_client, user_factory, event_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, pertencente ao usuário.
    event = event_factory(slug="event-a", owners=[user])

    # E DADO um track existente no banco.
    track = Track.objects.create(event=event, slug="track-a", name="Track A")

    # QUANDO a API é chamada para deletar o track.
    delete_resp = api_client.delete(reverse("track-detail", args=[track.slug]))

    # ENTÃO a deleção deverá ter sucesso.
    assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

    # E ENTÃO o track não existirá no banco.
    assert Track.available_objects.count() == 0

    # E QUANDO a API é chamada para obter o track deletado.
    retrieve_resp = api_client.get(reverse("track-detail", args=[track.slug]))

    # ENTÃO o track não será encontrado.
    assert retrieve_resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_unauthorized(api_client, user_factory, event_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento existente no banco, não pertencente ao usuário.
    event = event_factory(slug="event-a", owners=[])

    # E DADO um track existente no evento.
    track = Track.objects.create(event=event, slug="track-a", name="Track A")

    # QUANDO a API é chamada para deletar o track.
    resp = api_client.delete(reverse("track-detail", args=[track.slug]))

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # E ENTÃO o track não deve ser deletado.
    assert Track.objects.count() == 1
