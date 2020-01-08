from unittest import mock
from unittest.mock import Mock

import pytest

from eventos2.core.services import (
    event_registration_type as event_registration_type_service,
)
from eventos2.utils.exceptions import NotAuthorizedError, NotFoundError


@mock.patch("eventos2.core.services.event_registration_type.EventRegistrationType")
def test_get_by_id_valid(mock_registration_type):
    # DADO que o banco retorna um registration type
    expected_registration_type = Mock()
    mock_registration_type.objects.get.return_value = expected_registration_type

    # QUANDO obter um registration type com um ID qualquer
    registration_type = event_registration_type_service.get_by_id(123)

    # ENTÃO o banco deve ser consultado com esse ID
    assert mock_registration_type.objects.get.call_args == mock.call(pk=123)
    # E ENTÃO o registration type retornado deve ser o mesmo que o ORM retornou
    assert registration_type is expected_registration_type


@mock.patch("eventos2.core.services.event_registration_type.EventRegistrationType")
def test_get_by_id_invalid(mock_registration_type):
    # DADO que o banco não retorna um registration type (gera exceção)
    mock_registration_type.DoesNotExist = Exception
    mock_registration_type.objects.get.side_effect = mock_registration_type.DoesNotExist

    # QUANDO tentar obter um registration type com um ID qualquer
    # ENTÃO o serviço deve gerar sua própria exceção
    with pytest.raises(NotFoundError):
        event_registration_type_service.get_by_id(123)


@mock.patch("eventos2.core.services.event_registration_type.EventRegistrationType")
def test_create_valid(mock_registration_type):
    # DADO que o banco aceita criar qualquer registration type, e o retorna
    expected_registration_type = Mock()
    mock_registration_type.objects.create.return_value = expected_registration_type

    # E DADO um usuário que tem permissões
    actor = Mock()
    actor.has_perm.return_value = True

    # E DADO um evento
    event = Mock()

    # QUANDO criar um registration type
    registration_type = event_registration_type_service.create(
        actor=actor, event=event, name="Registration type A"
    )

    # ENTÃO o ORM deve ser chamado para criar o registration type
    assert mock_registration_type.objects.create.call_count == 1

    # E ENTÃO o registration type deve ser retornado
    assert registration_type is expected_registration_type


@mock.patch("eventos2.core.services.event_registration_type.EventRegistrationType")
def test_create_unauthorized(mock_registration_type):
    # DADO um usuário que não tem permissão alguma
    actor = Mock()
    actor.has_perm.return_value = False

    # E DADO um evento
    event = Mock()

    # QUANDO tentar criar um registration type
    # ENTÃO o serviço deverá gerar sua exeção de falta de permissões
    with pytest.raises(NotAuthorizedError):
        event_registration_type_service.create(
            actor=actor, event=event, name="Registration type A"
        )


@mock.patch("eventos2.core.services.event_registration_type.get_by_id")
def test_update_unauthorized(mock_get_by_id):
    # DADO que o registration type a ser editado existe
    registration_type = Mock()
    mock_get_by_id.return_value = registration_type

    # E DADO um usuário que não tem permissão alguma
    actor = Mock()
    actor.has_perm.return_value = False

    # QUANDO tentar editar o registration type
    # ENTÃO o serviço deve gerar sua exceção de falta de permissões
    with pytest.raises(NotAuthorizedError):
        event_registration_type_service.update(
            actor=actor, event_registration_type_id=123, name="New name",
        )


@mock.patch("eventos2.core.services.event_registration_type.get_by_id")
def test_delete_valid(mock_get_by_id):
    # DADO que o registration type a ser deletado existe
    registration_type = Mock()
    mock_get_by_id.return_value = registration_type

    # E DADO um usuário que tem permissões
    actor = Mock()
    actor.has_perm.return_value = True

    # QUANDO deletar o registration type
    event_registration_type_service.delete(actor=actor, event_registration_type_id=1)

    # ENTÃO o ORM deve ser chamado
    assert registration_type.delete.call_count == 1


@mock.patch("eventos2.core.services.event_registration_type.get_by_id")
def test_delete_unauthorized(mock_get_by_id):
    # DADO que o registration type a ser deletado existe
    registration_type = Mock()
    mock_get_by_id.return_value = registration_type

    # E DADO um usuário que não tem permissão alguma
    actor = Mock()
    actor.has_perm.return_value = False

    # QUANDO tentar deletar o registration type
    # ENTÃO o serviço deve gerar sua exceção de falta de permissões
    with pytest.raises(NotAuthorizedError):
        event_registration_type_service.delete(
            actor=actor, event_registration_type_id=1
        )


@mock.patch("eventos2.core.services.event_registration_type.EventRegistration")
@mock.patch("eventos2.core.services.event_registration_type.get_by_id")
def test_find_registrations_valid(mock_get_by_id, mock_eventregistration):
    # DADO um registration type
    registration_type = Mock()
    mock_get_by_id.return_value = registration_type

    # E DADO um usuário que tem permissões
    actor = Mock()
    actor.has_perm.return_value = True

    # E DADO que o banco retorna inscrições
    expected_registrations = Mock()
    mock_eventregistration.objects.filter.return_value = expected_registrations

    # QUANDO listar as inscrições do registration type
    registrations = event_registration_type_service.find_registrations(
        actor=actor, event_registration_type_id=1
    )

    # ENTÃO as inscrições serão retornadas
    assert registrations is expected_registrations


@mock.patch("eventos2.core.services.event_registration_type.get_by_id")
def test_find_registrations_unauthorized(mock_get_by_id):
    # DADO um registration type
    registration_type = Mock()
    mock_get_by_id.return_value = registration_type

    # E DADO um usuário que não tem permissão alguma
    actor = Mock()
    actor.has_perm.return_value = False

    # QUANDO tentar listar as inscrições o registration type
    # ENTÃO o serviço deve gerar sua exceção de falta de permissões
    with pytest.raises(NotAuthorizedError):
        event_registration_type_service.find_registrations(
            actor=actor, event_registration_type_id=1
        )
