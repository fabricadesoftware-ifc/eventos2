import pytest
from django.urls import reverse
from rest_framework import status

from eventos2.core.models import User


@pytest.mark.django_db
def test_create_valid(api_client):
    # DADO dados válidos para um user.
    # QUANDO a API é chamada para criar o user.
    resp = api_client.post(
        reverse("user-list"),
        {
            "email": "user@example.com",
            "password": "an-example-password",
            "first_name": "User",
            "last_name": "Example",
        },
    )

    # ENTÃO a resposta de sucesso deve conter os dados do usuário.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["email"] == "user@example.com"

    # E ENTÃO o usuário deve existir.
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_create_duplicate_user(api_client, user_factory):
    # DADO um usuário existente.
    existing_user = user_factory(name="user_a", permissions=[])

    # QUANDO a API é chamada para criar o user, com o mesmo email.
    resp = api_client.post(
        reverse("user-list"),
        {
            "email": existing_user.email,
            "password": "an-example-password",
            "first_name": "User",
            "last_name": "Example",
        },
    )

    # ENTÃO a resposta de falha deve conter o erro no campo email.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["email"]) != 0

    # E ENTÃO o usuário não deve ser criado.
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_list_valid(api_client, user_factory):
    # DADO dois usuário, um deles autenticado.
    user_a = user_factory(name="user-a", permissions=[])
    api_client.force_authenticate(user=user_a)
    user_b = user_factory(name="user-b", permissions=[])

    # QUANDO a API é chamada para buscar pelo user b.
    resp = api_client.get("{}?email={}".format(reverse("user-list"), user_b.email))

    # ENTÃO a resposta deve ser de sucesso e conter o user b.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data[0]["public_id"] == user_b.public_id


@pytest.mark.django_db
def test_list_unauthorized(api_client, user_factory):
    # DADO nenhum usuário autenticado.

    # QUANDO a API é chamada para buscar por um usuário.
    resp = api_client.get(
        "{}?email={}".format(reverse("user-list"), "example@example.com")
    )

    # ENTÃO a resposta deve ser de falta de permissão.
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_retrieve_current_valid(api_client, user_factory):
    # DADO um user autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # QUANDO a API é chamada para obter o user atual.
    resp = api_client.get(reverse("user-current"))

    # ENTÃO a resposta deve ser de sucesso.
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_retrieve_current_invalid(api_client, user_factory):
    # DADO nenhum user autenticado.

    # QUANDO a API é chamada para obter o user atual.
    resp = api_client.get(reverse("user-current"))

    # ENTÃO a resposta deve ser falta de permissão
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_current_valid(api_client, user_factory):
    # DADO um user autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # QUANDO a API é chamada para editar o user atual.
    resp = api_client.put(
        reverse("user-current"),
        {
            "first_name": "New first name",
            "last_name": "New last name",
            "email": "user@example.com",
        },
    )
    # ENTÃO a resposta de sucesso deve conter o user modificado.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["first_name"] == "New first name"
    # E ENTÃO o user deve ser modificado.
    assert User.objects.get(pk=user.pk).first_name == "New first name"


@pytest.mark.django_db
def test_update_current_invalid(api_client):
    # DADO nenhum user autenticado.

    # QUANDO a API é chamada para editar o user atual.
    resp = api_client.put(
        reverse("user-current"),
        {"first_name": "New first name", "last_name": "New last name"},
    )

    # ENTÃO a resposta deve ser falta de permissão
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_current_valid(api_client, user_factory):
    # DADO um user autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # QUANDO a API é chamada para remover o user atual.
    resp = api_client.delete(reverse("user-current"))

    # ENTÃO a resposta deve ser de sucesso.
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    # E ENTÃO o user deve ser removido.
    assert User.objects.filter(pk=user.pk).exists() is False


@pytest.mark.django_db
def test_delete_current_invalid(api_client):
    # DADO nenhum user autenticado.

    # QUANDO a API é chamada para remover o user atual.
    resp = api_client.delete(reverse("user-current"))

    # ENTÃO a resposta deve ser falta de permissão
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_list_submissions_current(
    api_client, user_factory, event_factory, track_factory, submission_factory
):
    # DADO um user autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    # E DADO uma submissão do user
    event = event_factory(slug="Event A", owners=[])
    track = track_factory(event=event, name="Track A")
    submission = submission_factory(track=track, title="Submission A", authors=[user])

    # QUANDO a API é chamada para listar as submissões do user atual.
    resp = api_client.get(reverse("user-current-list-submissions"))

    # ENTÃO a resposta deve ser de sucesso.
    assert resp.status_code == status.HTTP_200_OK
    # E ENTÃO a resposta deve conter a submissão do user.
    assert len(resp.data) == 1
    assert resp.data[0]["title"] == submission.title


@pytest.mark.django_db
def test_list_review_requests(
    api_client,
    user_factory,
    event_factory,
    track_factory,
    submission_factory,
    review_factory,
):
    # DADO um user autenticado.
    user = user_factory(name="User A", permissions=[])
    api_client.force_authenticate(user=user)
    # E DADO uma submissão de outro user
    event = event_factory(slug="Event A", owners=[])
    track = track_factory(event=event, name="Track A")
    other_user = user_factory(name="User B", permissions=[])
    submission = submission_factory(
        track=track, title="Submission A", authors=[other_user]
    )
    # E DADO uma review pendente.
    review_factory(submission=submission, author=user)

    # QUANDO a API é chamada para listar as reviews pendentes do user atual.
    resp = api_client.get(reverse("user-current-list-review-requests"))

    # ENTÃO a resposta deve ser de sucesso.
    assert resp.status_code == status.HTTP_200_OK
    # E ENTÃO a resposta deve conter a submissão pendente a ser avaliada pelo usuário.
    assert len(resp.data) == 1
    assert resp.data[0]["submission"]["title"] == submission.title
