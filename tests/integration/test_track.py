import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from eventos2.core.models import Track


@pytest.mark.django_db
def test_create_valid(api_client, user_factory, event_factory):
    # DADO um usuário autenticado, e um evento pertencente a ele.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[user])

    # E DADO dados de track válidos.
    # QUANDO a API é chamada.
    resp = api_client.post(
        reverse("track-list"),
        {
            "event_slug": event.slug,
            "slug": "track-a",
            "name": "Track A",
            "starts_on": timezone.now(),
            "ends_on": timezone.now(),
        },
    )

    # ENTÃO a resposta de sucesso deve conter os dados do track.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["slug"] == "track-a"
    # E ENTÃO o track deve existir.
    assert Track.objects.get(slug=resp.data["slug"]).name == "Track A"


@pytest.mark.django_db
def test_create_unauthorized(api_client, user_factory, event_factory):
    # DADO um usuário, e um evento não pertencente a ele.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])

    # QUANDO a API é chamada para criar um track.
    resp = api_client.post(
        reverse("track-list"),
        {
            "event_slug": event.slug,
            "slug": "track-a",
            "name": "Track A",
            "starts_on": timezone.now(),
            "ends_on": timezone.now(),
        },
    )

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO o track não deve ser criado.
    assert Track.objects.count() == 0


@pytest.mark.django_db
def test_create_duplicate_slug(api_client, user_factory, event_factory, track_factory):
    # DADO um usuário autenticado, um evento pertencente a ele, e um track no evento.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[user])
    existing_track = track_factory(event=event, slug="track-a")

    # QUANDO a API é chamada para criar um track com o mesmo slug.
    resp = api_client.post(
        reverse("track-list"),
        {
            "event_slug": event.slug,
            "slug": existing_track.slug,
            "name": "Track B",
            "starts_on": timezone.now(),
            "ends_on": timezone.now(),
        },
    )

    # ENTÃO a resposta de falha deve conter o erro no campo slug.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["slug"]) != 0
    # E ENTÃO o track não deve ser criado.
    assert Track.objects.count() == 1


@pytest.mark.django_db
def test_retrieve_valid(api_client, user_factory, event_factory, track_factory):
    # DADO um usuário, um evento, e um track.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    track = track_factory(event=event, slug="track-a")

    # QUANDO a API é chamada para obter o track.
    resp = api_client.get(reverse("track-detail", args=[track.slug]))

    # ENTÃO a resposta de sucesso deve conter os dados do track.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["slug"] == track.slug


@pytest.mark.django_db
def test_retrieve_unauthorized(api_client, event_factory, track_factory):
    # DADO nenhum usuário autenticado.
    # E DADO um evento e um track.
    event = event_factory(slug="event-a", owners=[])
    track = track_factory(event=event, slug="track-a")

    # QUANDO a API é chamada para obter o track.
    resp = api_client.get(reverse("track-detail", args=[track.slug]))

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_valid(api_client, user_factory, event_factory, track_factory):
    # DADO um usuário autenticado, um evento pertencente a ele, e um track no evento.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[user])
    track = track_factory(event=event, slug="track-a")

    # E DADO dados de track válidos.
    # QUANDO a API é chamada.
    resp = api_client.put(
        reverse("track-detail", args=[track.slug]),
        {
            "slug": "{} modified!".format(track.slug),
            "name": track.name,
            "starts_on": track.starts_on,
            "ends_on": track.ends_on,
        },
    )

    # ENTÃO a reposta de sucesso deve conter o track modificado.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["name"] == track.name
    assert resp.data["slug"] == "{} modified!".format(track.slug)
    # E ENTÃO o track deve ser modificado.
    assert Track.objects.get(pk=track.id).slug == "{} modified!".format(track.slug)
    assert Track.objects.count() == 1


@pytest.mark.django_db
def test_update_duplicate_slug(api_client, user_factory, event_factory, track_factory):
    # DADO um usuário autenticado, um evento pertencente a ele, e dois tracks no evento.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[user])
    track_a = track_factory(event=event, slug="track-a")
    track_b = track_factory(event=event, slug="track-b")

    # E DADO dados de track inválidos (valor de slug utilizado pelo track A).
    # QUANDO a API é chamada.
    resp = api_client.put(
        reverse("track-detail", args=[track_b.slug]),
        {"slug": track_a.slug, "name": track_b.name},
    )

    # ENTÃO a resposta de falha deve conter o erro no campo slug.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["slug"]) != 0
    # E ENTÃO o track não deve ser modificado.
    assert Track.objects.get(pk=track_b.id).slug == track_b.slug


@pytest.mark.django_db
def test_update_unauthorized(api_client, user_factory, event_factory, track_factory):
    # DADO um usuário autenticado, um evento não pertencente a ele,
    # e um track no evento.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    track = track_factory(event=event, slug="track-a")

    # QUANDO a API é chamada para editar o track.
    resp = api_client.put(
        reverse("track-detail", args=[track.slug]),
        {"slug": track.slug, "name": track.name + " modified"},
    )

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO o track não deve ser modificado.
    assert Track.objects.get(pk=track.id).name == track.name


@pytest.mark.django_db
def test_delete_valid(api_client, user_factory, event_factory, track_factory):
    # DADO um usuário autenticado, e um evento pertencente a ele, e um track no evento.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[user])
    track = track_factory(event=event, slug="track-a")

    # QUANDO a API é chamada para deletar o track.
    delete_resp = api_client.delete(reverse("track-detail", args=[track.slug]))

    # ENTÃO a deleção deverá ter sucesso.
    assert delete_resp.status_code == status.HTTP_204_NO_CONTENT
    # E ENTÃO o track não existirá.
    assert Track.available_objects.count() == 0

    # E QUANDO a API é chamada para obter o track deletado.
    retrieve_resp = api_client.get(reverse("track-detail", args=[track.slug]))

    # ENTÃO o track não será encontrado.
    assert retrieve_resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_unauthorized(api_client, user_factory, event_factory, track_factory):
    # DADO um usuário autenticado, um evento não pertencente a ele,
    # e um track no evento.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    track = track_factory(event=event, slug="track-a")

    # QUANDO a API é chamada para deletar o track.
    resp = api_client.delete(reverse("track-detail", args=[track.slug]))

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO o track não deve ser deletado.
    assert Track.objects.count() == 1


@pytest.mark.django_db
def test_list_submissions(
    api_client, user_factory, event_factory, track_factory, submission_factory
):
    # DADO um usuário autenticado, um evento pertencente a ele, e um track no evento.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[user])
    track = track_factory(event=event, slug="track-a")
    # E DADO uma submission no track.
    submission_a = submission_factory(track=track, title="Submission A", authors=[])

    # QUANDO a API é chamada para listar as submissions do track.
    resp = api_client.get(reverse("track-list-submissions", args=[track.slug]))

    # ENTÃO as submissions serão retornadas
    assert resp.status_code == status.HTTP_200_OK

    assert len(resp.data) == 1
    assert resp.data[0]["title"] == submission_a.title


@pytest.mark.django_db
def test_list_submission_document_slots(
    api_client,
    user_factory,
    event_factory,
    track_factory,
    track_submission_document_slot_factory,
):
    # DADO um usuário autenticado, um evento pertencente a ele, e um track no evento.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[user])
    track = track_factory(event=event, slug="track-a")
    # E DADO um submission document slot no track.
    slot_a = track_submission_document_slot_factory(track=track, name="Slot A")

    # QUANDO a API é chamada para listar os slots do track.
    resp = api_client.get(
        reverse("track-list-submission-document-slots", args=[track.slug])
    )

    # ENTÃO os slots serão retornados
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data) == 1
    assert resp.data[0]["name"] == slot_a.name
