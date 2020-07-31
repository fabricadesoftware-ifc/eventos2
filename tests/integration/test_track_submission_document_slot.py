import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from eventos2.core.models import TrackSubmissionDocumentSlot


@pytest.mark.django_db
def test_create_valid(api_client, user_factory, event_factory, track_factory):
    # DADO um usuário autenticado, um evento pertencente a ele, e um track no evento.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[user])
    track = track_factory(event=event, slug="track-a")

    # E DADO dados de slot válidos.
    # QUANDO a API é chamada.
    resp = api_client.post(
        reverse("track-submission-document-slot-list"),
        {
            "track_slug": track.slug,
            "name": "Slot A",
            "starts_on": timezone.now(),
            "ends_on": timezone.now(),
        },
    )

    # ENTÃO a resposta de sucesso deve conter os dados do slot.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["name"] == "Slot A"
    # E ENTÃO o slot deve existir.
    assert TrackSubmissionDocumentSlot.objects.get(id=resp.data["id"]).name == "Slot A"


@pytest.mark.django_db
def test_create_unauthorized(api_client, user_factory, event_factory, track_factory):
    # DADO um usuário autenticado, um evento não pertencente a ele,
    # e um track no evento.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    track = track_factory(event=event, slug="track-a")

    # E DADO dados de slot válidos.
    # QUANDO a API é chamada.
    resp = api_client.post(
        reverse("track-submission-document-slot-list"),
        {
            "track_slug": track.slug,
            "name": "Slot A",
            "starts_on": timezone.now(),
            "ends_on": timezone.now(),
        },
    )

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO o slot não deve ser criado.
    assert TrackSubmissionDocumentSlot.objects.count() == 0


@pytest.mark.django_db
def test_update_valid(
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
    # E DADO um slot existente no track.
    slot = track_submission_document_slot_factory(track=track, name="Slot A")

    # E DADO dados de slot válidos.
    # QUANDO a API é chamada.
    resp = api_client.put(
        reverse("track-submission-document-slot-detail", args=[slot.id]),
        {
            "name": "{} modified!".format(slot.name),
            "starts_on": slot.starts_on,
            "ends_on": slot.ends_on,
        },
    )

    # ENTÃO a reposta de sucesso deve conter o slot modificado.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["name"] == "{} modified!".format(slot.name)
    # E ENTÃO o slot deve ser modificado.
    assert TrackSubmissionDocumentSlot.objects.get(
        pk=slot.id
    ).name == "{} modified!".format(slot.name)
    assert TrackSubmissionDocumentSlot.objects.count() == 1


@pytest.mark.django_db
def test_update_unauthorized(
    api_client,
    user_factory,
    event_factory,
    track_factory,
    track_submission_document_slot_factory,
):
    # DADO um usuário autenticado, um evento não pertencente a ele,
    # e um track no evento.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    track = track_factory(event=event, slug="track-a")
    # E DADO um slot existente no track.
    slot = track_submission_document_slot_factory(track=track, name="Slot A")

    # E DADO dados de slot válidos.
    # QUANDO a API é chamada.
    resp = api_client.put(
        reverse("track-submission-document-slot-detail", args=[slot.id]),
        {
            "name": "{} modified!".format(slot.name),
            "starts_on": slot.starts_on,
            "ends_on": slot.ends_on,
        },
    )

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO o slot não deve ser modificado.
    assert TrackSubmissionDocumentSlot.objects.get(pk=slot.id).name == slot.name


@pytest.mark.django_db
def test_delete_valid(
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
    # E DADO um slot existente no track.
    slot = track_submission_document_slot_factory(track=track, name="Slot A")

    # E DADO dados de slot válidos.
    # QUANDO a API é chamada para deletar o slot.
    delete_resp = api_client.delete(
        reverse("track-submission-document-slot-detail", args=[slot.id])
    )

    # ENTÃO a deleção deverá ter sucesso.
    assert delete_resp.status_code == status.HTTP_204_NO_CONTENT
    # E ENTÃO o track não existirá.
    assert TrackSubmissionDocumentSlot.objects.count() == 0


@pytest.mark.django_db
def test_delete_unauthorized(
    api_client,
    user_factory,
    event_factory,
    track_factory,
    track_submission_document_slot_factory,
):
    # DADO um usuário autenticado, um evento não pertencente a ele,
    # e um track no evento.
    user = user_factory(name="user", permissions=["core.change_event"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    track = track_factory(event=event, slug="track-a")
    # E DADO um slot existente no track.
    slot = track_submission_document_slot_factory(track=track, name="Slot A")

    # E DADO dados de slot válidos.
    # QUANDO a API é chamada para deletar o slot.
    resp = api_client.delete(
        reverse("track-submission-document-slot-detail", args=[slot.id])
    )

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO o slot não deve ser deletado.
    assert TrackSubmissionDocumentSlot.objects.count() == 1
