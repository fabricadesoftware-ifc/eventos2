import pytest
from django.urls import reverse
from rest_framework import status

from eventos2.core.models import SubmissionDocument
from eventos2.utils.files import CONTENT_TYPE_PDF


@pytest.mark.django_db
def test_create_valid(
    api_client,
    user_factory,
    event_factory,
    document_factory,
    submission_factory,
    track_factory,
    track_submission_document_slot_factory,
):
    # DADO um usuário autenticado, e um evento com track e slot.
    user = user_factory(name="user", permissions=["core.change_submission"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    track = track_factory(event=event, name="Track A")
    slot = track_submission_document_slot_factory(track=track, name="Slot A")
    # E DADO uma submissão do usuário no track.
    submission = submission_factory(track=track, title="Submission A", authors=[user])
    # E DADO um document
    document = document_factory(file_path="fake.pdf", content_type=CONTENT_TYPE_PDF)

    # E DADO dados válidos.
    # QUANDO a API é chamada.
    resp = api_client.post(
        reverse("submission-document-list"),
        {
            "submission": submission.id,
            "slot": slot.id,
            "document_attachment_key": document.attachment_key,
        },
    )

    # ENTÃO a resposta de sucesso deve conter a data de submissão.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["submitted_on"]
    # E então a submission document deve ser criada.
    assert SubmissionDocument.objects.count() == 1


@pytest.mark.django_db
def test_create_unauthorized(
    api_client,
    user_factory,
    event_factory,
    document_factory,
    submission_factory,
    track_factory,
    track_submission_document_slot_factory,
):
    # DADO um usuário autenticado, e um evento com track e slot.
    user = user_factory(name="user", permissions=["core.change_submission"])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    track = track_factory(event=event, name="Track A")
    slot = track_submission_document_slot_factory(track=track, name="Slot A")
    # E DADO uma submissão não pertencente ao usuário no track.
    submission = submission_factory(track=track, title="Submission A", authors=[])
    # E DADO um document
    document = document_factory(file_path="fake.pdf", content_type=CONTENT_TYPE_PDF)

    # E DADO dados válidos.
    # QUANDO a API é chamada.
    resp = api_client.post(
        reverse("submission-document-list"),
        {
            "submission": submission.id,
            "slot": slot.id,
            "document_attachment_key": document.attachment_key,
        },
    )

    # ENTÃO a resposta deve ser de falta de permissões.
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO a submissão não deve ser criada.
    assert SubmissionDocument.objects.count() == 0


@pytest.mark.django_db
def test_create_out_of_submission_period(
    api_client,
    track_factory,
    track_submission_document_slot_factory,
    event_factory,
    submission_factory,
    document_factory,
    user_factory,
    freezer,
    parse_to_aware_datetime,
):
    # DADO um usuário autenticado, e um evento com track e slot.
    user = user_factory(name="user", permissions=["core.change_submission"])
    api_client.force_authenticate(user=user)
    event = event_factory(
        slug="event-a",
        owners=[],
        starts_on=parse_to_aware_datetime("2020-01-01"),
        ends_on=parse_to_aware_datetime("2020-02-02"),
    )
    track = track_factory(
        event=event, name="Track A", starts_on=event.starts_on, ends_on=event.ends_on
    )
    slot = track_submission_document_slot_factory(
        track=track, name="Slot A", starts_on=event.starts_on, ends_on=event.ends_on
    )
    # E DADO uma submissão do usuário no track.
    submission = submission_factory(track=track, title="Submission A", authors=[user])
    # E DADO um document
    document = document_factory(file_path="fake.pdf", content_type=CONTENT_TYPE_PDF)

    # E DADO que já passou o tempo de submissão
    freezer.move_to(parse_to_aware_datetime("2020-03-03"))
    # QUANDO a API é chamada.
    resp = api_client.post(
        reverse("submission-document-list"),
        {
            "submission": submission.id,
            "slot": slot.id,
            "document_attachment_key": document.attachment_key,
        },
    )

    # ENTÃO a reposta de falha deve conter o erro no campo slot.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["slot"]) != 0
    # E ENTÃO a submissão não deve ser criada.
    assert SubmissionDocument.objects.count() == 0
