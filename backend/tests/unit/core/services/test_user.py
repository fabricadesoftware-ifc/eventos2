from unittest import mock
from unittest.mock import Mock

import pytest

from eventos2.core.services import user as user_service
from eventos2.utils.exceptions import (
    DuplicateIdentifierError,
    NotAuthorizedError,
    NotFoundError,
)


@mock.patch("eventos2.core.services.user.User")
def test_get_by_id_valid(mock_user):
    # DADO que o banco retorna um user
    expected_user = Mock()
    mock_user.objects.get.return_value = expected_user

    # QUANDO obter um user com um ID qualquer
    user = user_service.get_by_id(123)

    # ENTÃO o banco deve ser consultado com esse ID
    assert mock_user.objects.get.call_args == mock.call(pk=123)
    # E ENTÃO o user retornado deve ser o mesmo que o ORM retornou
    assert user is expected_user


@mock.patch("eventos2.core.services.user.User")
def test_get_by_id_must_be_active(mock_user):
    # DADO que o banco não retorna um user quando filtrado (gera exceção)
    mock_user.objects.filter.return_value = mock_user.objects
    mock_user.DoesNotExist = Exception
    mock_user.objects.get.side_effect = mock_user.DoesNotExist

    # QUANDO obter um user com um ID qualquer, e filtrar por active
    # ENTÃO o serviço deve gerar sua própria exceção
    with pytest.raises(NotFoundError):
        user_service.get_by_id(123, must_be_active=True)


@mock.patch("eventos2.core.services.user.User")
def test_exists_by_email_valid(mock_user):
    # DADO que o banco afirma que a toda consulta tem resultados
    mock_user.objects.filter.return_value = mock_user.objects
    mock_user.objects.exists.return_value = True

    # QUANDO verificar se existe um user com um email
    # ENTÃO o serviço deve afirmar que sim
    assert user_service.exists_by_email("user@example.com") is True


@mock.patch("eventos2.core.services.user.User")
def test_exists_by_email_invalid(mock_user):
    # DADO que o banco afirma que a toda consulta não tem resultados
    mock_user.objects.filter.return_value = mock_user.objects
    mock_user.objects.exists.return_value = False

    # QUANDO verificar se existe um user com um email
    # ENTÃO o serviço deve afirmar que não
    assert user_service.exists_by_email("user@example.com") is False


@mock.patch("eventos2.core.services.user.User")
@mock.patch("eventos2.core.services.user.exists_by_email")
def test_create_valid(mock_exists_by_email, mock_user):
    # DADO que o banco aceita criar qualquer user, e o retorna
    expected_user = Mock()
    mock_user.objects.create.return_value = expected_user

    # E DADO que não existem users
    mock_exists_by_email.return_value = False

    # QUANDO registrar um usuário
    user = user_service.create(
        email="user@example.com",
        password="hunter2",
        first_name="User",
        last_name="Example",
    )

    # ENTÃO o ORM deve ser chamado para criar o usuário
    assert mock_user.objects.create.call_count == 1

    # E ENTÃO o usuário deve ser retornado
    assert user is expected_user


@mock.patch("eventos2.core.services.user.User")
@mock.patch("eventos2.core.services.user.exists_by_email")
def test_create_duplicate(mock_exists_by_email, mock_user):
    # DADO que haverá uma colisão
    # (user já existe com esse email)
    mock_exists_by_email.return_value = True

    # QUANDO tentar registrar um usuário com o mesmo email
    # ENTÃO o serviço deve gerar sua exceção de colisão
    with pytest.raises(DuplicateIdentifierError):
        user_service.create(
            email="user@example.com",
            password="hunter2",
            first_name="User",
            last_name="Example",
        )


@mock.patch("eventos2.core.services.user.get_by_id")
def test_update_unauthorized(mock_get_by_id):
    # DADO um usuário que não tem permissão alguma
    actor = Mock()
    actor.has_perm.return_value = False

    # E DADO que ele será editado
    mock_get_by_id.return_value = actor

    # QUANDO tentar editar
    # ENTÃO o serviço deve gerar sua exceção de falta de permissões
    with pytest.raises(NotAuthorizedError):
        user_service.update(
            actor=actor,
            user_id=123,
            first_name="New first name",
            last_name="New last name",
        )


@mock.patch("eventos2.core.services.user.get_by_id")
def test_delete_valid(mock_get_by_id):
    # DADO um usuário que tem permissões
    actor = Mock()
    actor.has_perm.return_value = True

    # E DADO que ele será deletado
    mock_get_by_id.return_value = actor

    # QUANDO deletar
    user_service.delete(
        actor=actor, user_id=123,
    )

    # ENTÃO o ORM deve ser chamado
    actor.delete.call_count == 1


@mock.patch("eventos2.core.services.user.get_by_id")
def test_delete_unauthorized(mock_get_by_id):
    # DADO um usuário que não tem permissão alguma
    actor = Mock()
    actor.has_perm.return_value = False

    # E DADO que ele será deletado
    mock_get_by_id.return_value = actor

    # QUANDO tentar editar
    # ENTÃO o serviço deve gerar sua exceção de falta de permissões
    with pytest.raises(NotAuthorizedError):
        user_service.delete(
            actor=actor, user_id=123,
        )
