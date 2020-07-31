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
