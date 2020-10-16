import pytest
from django.urls import reverse
from rest_framework import status

from eventos2.core.models import EventRegistration, Submission
from eventos2.utils.files import CONTENT_TYPE_PDF


@pytest.mark.django_db
def test_submit_valid(
    api_client,
    track_factory,
    event_factory,
    user_factory,
    track_submission_document_slot_factory,
    document_factory,
):
    # DADO um usuário autenticado, e um evento no qual ele está registrado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    EventRegistration.objects.create(event=event, user=user)
    # E DADO um track com slot no evento.
    track = track_factory(event=event, name="Track A")
    slot = track_submission_document_slot_factory(track=track, name="Slot A")
    # E DADO um document.
    document = document_factory(file_path="fake.pdf", content_type=CONTENT_TYPE_PDF)
    # E DADO um segundo usuário.
    other_user = user_factory(name="other-user", permissions=[])

    # QUANDO a API é chamada para submeter no track.
    resp = api_client.post(
        reverse("submission-list"),
        {
            "track": track.id,
            "title": "Title",
            "other_authors": [other_user.public_id],
            "documents": [
                {"slot": slot.id, "document_attachment_key": document.attachment_key}
            ],
        },
    )

    # ENTÃO a reposta deve ser de sucesso
    assert resp.status_code == status.HTTP_201_CREATED
    # E ENTÃO o submission deve ser criado.
    assert Submission.objects.count() == 1
    assert Submission.objects.first().authors.count() == 2
    # E ENTÃO a relação com o document deve ser criada.
    assert Submission.objects.first().documents.first().document == document


@pytest.mark.django_db
def test_submit_not_registered_to_event(
    api_client, track_factory, event_factory, user_factory
):
    # DADO um usuário autenticado, um evento no qual ele não está registrado,
    # e um track no evento.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    track = track_factory(event=event, name="Track A")

    # QUANDO a API é chamada para submeter no track.
    resp = api_client.post(
        reverse("submission-list"), {"track": track.id, "title": "Title"}
    )

    # ENTÃO a reposta deve ser de falta de permissões
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO o submission não deve ser criado.
    assert Submission.objects.count() == 0


@pytest.mark.django_db
def test_submit_out_of_submission_period(
    api_client,
    track_factory,
    event_factory,
    user_factory,
    freezer,
    parse_to_aware_datetime,
):
    # DADO um usuário autenticado, um evento no qual ele está registrado,
    # e um track no evento.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event = event_factory(
        slug="event-a",
        owners=[],
        starts_on=parse_to_aware_datetime("2020-01-01"),
        ends_on=parse_to_aware_datetime("2020-02-02"),
    )
    EventRegistration.objects.create(event=event, user=user)
    track = track_factory(
        event=event, name="Track A", starts_on=event.starts_on, ends_on=event.ends_on
    )
    # E DADO que já passou o tempo de submissão
    freezer.move_to(parse_to_aware_datetime("2020-03-03"))

    # QUANDO a API é chamada para submeter no track.
    resp = api_client.post(
        reverse("submission-list"), {"track": track.id, "title": "Title"}
    )

    # ENTÃO a reposta de falha deve conter o erro no campo track.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["track"]) != 0
    # E ENTÃO o submission não deve ser criado.
    assert Submission.objects.count() == 0


@pytest.mark.django_db
def test_submit_missing_document(
    api_client,
    track_factory,
    event_factory,
    user_factory,
    track_submission_document_slot_factory,
):
    # DADO um usuário autenticado, e um evento no qual ele está registrado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    EventRegistration.objects.create(event=event, user=user)
    # E DADO um track com slot no evento.
    track = track_factory(event=event, name="Track A")
    track_submission_document_slot_factory(track=track, name="Slot A")

    # QUANDO a API é chamada para submeter no track.
    resp = api_client.post(
        reverse("submission-list"), {"track": track.id, "title": "Title"},
    )

    # ENTÃO a reposta de falha deve conter o erro no campo documents,
    # pois o slot A não foi preenchido.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["documents"]) != 0
    # E ENTÃO o submission não deve ser criado.
    assert Submission.objects.count() == 0


@pytest.mark.django_db
def test_submit_closed_slot(
    api_client,
    track_factory,
    event_factory,
    user_factory,
    track_submission_document_slot_factory,
    document_factory,
    freezer,
    parse_to_aware_datetime,
):
    # DADO um usuário autenticado, um evento no qual ele está registrado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event = event_factory(
        slug="event-a",
        owners=[],
        starts_on=parse_to_aware_datetime("2020-01-01"),
        ends_on=parse_to_aware_datetime("2020-04-04"),
    )
    EventRegistration.objects.create(event=event, user=user)
    # E DADO um track com dois slots no evento.
    track = track_factory(
        event=event, name="Track A", starts_on=event.starts_on, ends_on=event.ends_on
    )
    slot_a = track_submission_document_slot_factory(
        track=track, name="Slot A", starts_on=event.starts_on, ends_on=event.ends_on
    )
    slot_b = track_submission_document_slot_factory(
        track=track,
        name="Slot B",
        starts_on=parse_to_aware_datetime("2020-03-03"),
        ends_on=event.ends_on,
    )
    # E DADO um document.
    document = document_factory(file_path="fake.pdf", content_type=CONTENT_TYPE_PDF)

    # E DADO que não começou o tempo de submissão do slot B
    freezer.move_to(parse_to_aware_datetime("2020-02-02"))

    # QUANDO a API é chamada para submeter no track.
    resp = api_client.post(
        reverse("submission-list"),
        {
            "track": track.id,
            "title": "Title",
            "documents": [
                {"slot": slot_a.id, "document_attachment_key": document.attachment_key},
                {"slot": slot_b.id, "document_attachment_key": document.attachment_key},
            ],
        },
    )

    # ENTÃO a reposta de falha deve conter o erro no campo documents,
    # pois o slot B não está aberto.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["documents"]) != 0
    # E ENTÃO o submission não deve ser criado.
    assert Submission.objects.count() == 0


@pytest.mark.django_db
def test_submit_invalid_slot(
    api_client,
    track_factory,
    event_factory,
    user_factory,
    track_submission_document_slot_factory,
    document_factory,
):
    # DADO um usuário autenticado, e um evento no qual ele está registrado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    EventRegistration.objects.create(event=event, user=user)
    # E DADO dois tracks evento, um deles com slot.
    track_a = track_factory(event=event, name="Track A")
    slot_a = track_submission_document_slot_factory(track=track_a, name="Slot A")
    track_b = track_factory(event=event, name="Track B")
    # E DADO um document.
    document = document_factory(file_path="fake.pdf", content_type=CONTENT_TYPE_PDF)

    # QUANDO a API é chamada para submeter no track B, usando um slot do track A.
    resp = api_client.post(
        reverse("submission-list"),
        {
            "track": track_b.id,
            "title": "Title",
            "documents": [
                {"slot": slot_a.id, "document_attachment_key": document.attachment_key}
            ],
        },
    )

    # ENTÃO a reposta de falha deve conter o erro no campo documents,
    # pois o slot A não pertence ao track B.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["documents"]) != 0
    # E ENTÃO o submission não deve ser criado.
    assert Submission.objects.count() == 0
