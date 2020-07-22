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
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=["core.change_submission"])
    api_client.force_authenticate(user=user)

    # E DADO um evento com track e slot.
    event = event_factory(slug="event-a", owners=[])
    track = track_factory(event=event, slug="track-a")
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

    # E então a submission document deve ser criada no banco.
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
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=["core.change_submission"])
    api_client.force_authenticate(user=user)

    # E DADO um evento com track e slot.
    event = event_factory(slug="event-a", owners=[])
    track = track_factory(event=event, slug="track-a")
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

    # E ENTÃO a submissão não deve ser criada no banco.
    assert SubmissionDocument.objects.count() == 0
