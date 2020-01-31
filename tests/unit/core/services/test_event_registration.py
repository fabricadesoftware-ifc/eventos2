from unittest import mock
from unittest.mock import Mock

import pytest

from eventos2.core.services import event_registration as event_registration_service
from eventos2.utils.exceptions import ConflictError, NotAuthorizedError, NotFoundError


@mock.patch("eventos2.core.services.event_registration.EventRegistration")
def test_get_by_id_valid(mock_registration):
    # DADO que o banco retorna uma registration
    expected_registration = Mock()
    mock_registration.objects.get.return_value = expected_registration

    # QUANDO obter uma registration com um ID qualquer
    registration = event_registration_service.get_by_id(123)

    # ENTÃO o banco deve ser consultado com esse ID
    assert mock_registration.objects.get.call_args == mock.call(pk=123)
    # E ENTÃO o registration retornado deve ser o mesmo que o ORM retornou
    assert registration is expected_registration


@mock.patch("eventos2.core.services.event_registration.EventRegistration")
def test_get_by_id_invalid(mock_registration):
    # DADO que o banco não retorna uma registration (gera exceção)
    mock_registration.DoesNotExist = Exception
    mock_registration.objects.get.side_effect = mock_registration.DoesNotExist

    # QUANDO tentar obter uma registration com um ID qualquer
    # ENTÃO o serviço deve gerar sua própria exceção
    with pytest.raises(NotFoundError):
        event_registration_service.get_by_id(123)


@mock.patch("eventos2.core.services.event_registration.EventRegistration")
def test_exists_by_registration_type_and_user_valid(mock_registration):
    # DADO que o banco afirma que a toda consulta tem resultados
    mock_registration.objects.filter.return_value = mock_registration.objects
    mock_registration.objects.exists.return_value = True

    registration_type = Mock()
    user = Mock()

    # QUANDO verificar se existe um registration para um type e usuário qualquer
    # ENTÃO o serviço deve afirmar que sim
    assert (
        event_registration_service.exists_by_registration_type_and_user(
            registration_type, user
        )
        is True
    )


@mock.patch("eventos2.core.services.event_registration.EventRegistration")
def test_exists_by_registration_type_and_user_invalid(mock_registration):
    # DADO que o banco afirma que a toda consulta não tem resultados
    mock_registration.objects.filter.return_value = mock_registration.objects
    mock_registration.objects.exists.return_value = False

    registration_type = Mock()
    user = Mock()

    # QUANDO verificar se existe um registration para um type e usuário qualquer
    # ENTÃO o serviço deve afirmar que não
    assert (
        event_registration_service.exists_by_registration_type_and_user(
            registration_type, user
        )
        is False
    )


@mock.patch("eventos2.core.services.event_registration.EventRegistration")
@mock.patch(
    "eventos2.core.services.event_registration.exists_by_registration_type_and_user"
)
def test_register_self_valid(
    mock_exists_by_registration_type_and_user, mock_registration
):
    # DADO que o banco aceita criar qualquer registration, e o retorna
    expected_registration = Mock()
    mock_registration.objects.create.return_value = expected_registration

    # E DADO que não existem registrations
    mock_exists_by_registration_type_and_user.return_value = False

    # E DADO um usuário que tem permissões
    actor = Mock()
    actor.has_perm.return_value = True

    # E DADO um registration type
    registration_type = Mock()

    # QUANDO se registrar
    registration = event_registration_service.register(
        actor=actor, registration_type=registration_type, user=actor
    )

    # ENTÃO o ORM deve ser chamado para criar o registration
    assert mock_registration.objects.create.call_count == 1

    # E ENTÃO o registration deve ser retornado
    assert registration is expected_registration


@mock.patch("eventos2.core.services.event_registration.EventRegistration")
@mock.patch(
    "eventos2.core.services.event_registration.exists_by_registration_type_and_user"
)
def test_register_self_duplicate(
    mock_exists_by_registration_type_and_user, mock_registration
):
    # DADO que haverá uma colisão
    # (registration já existe)
    mock_exists_by_registration_type_and_user.return_value = True

    # E DADO um usuário que tem permissões
    actor = Mock()
    actor.has_perm.return_value = True

    # E DADO um registration type
    registration_type = Mock()

    # QUANDO tentar se registrar novamente
    # ENTÃO o serviço deve gerar sua exceção de colisão
    with pytest.raises(ConflictError):
        event_registration_service.register(
            actor=actor, registration_type=registration_type, user=actor
        )


@mock.patch("eventos2.core.services.event_registration.EventRegistration")
@mock.patch(
    "eventos2.core.services.event_registration.exists_by_registration_type_and_user"
)
def test_register_other_user_valid(
    mock_exists_by_registration_type_and_user, mock_registration
):
    # DADO que o banco aceita criar qualquer registration, e o retorna
    expected_registration = Mock()
    mock_registration.objects.create.return_value = expected_registration

    # E DADO que não existem registrations
    mock_exists_by_registration_type_and_user.return_value = False

    # E DADO um usuário que tem permissões
    actor = Mock()
    actor.has_perm.return_value = True

    # E DADO outro usuário alvo
    target = Mock()

    # E DADO um registration type
    registration_type = Mock()

    # QUANDO o actor tentar registrar o usuário alvo
    registration = event_registration_service.register(
        actor=actor, registration_type=registration_type, user=target
    )

    # ENTÃO o ORM deve ser chamado para criar o registration
    assert mock_registration.objects.create.call_count == 1

    # E ENTÃO o registration deve ser retornado
    assert registration is expected_registration


@mock.patch("eventos2.core.services.event_registration.EventRegistration")
def test_register_other_user_unauthorized(mock_registration):
    # DADO um usuário que não tem permissão alguma
    actor = Mock()
    actor.has_perm.return_value = False

    # E DADO outro usuário alvo
    target = Mock()

    # E DADO um registration type
    registration_type = Mock()

    # QUANDO o actor tentar registrar o usuário alvo
    # ENTÃO o serviço deverá gerar sua exeção de falta de permissões
    with pytest.raises(NotAuthorizedError):
        event_registration_service.register(
            actor=actor, registration_type=registration_type, user=target
        )


@mock.patch("eventos2.core.services.event_registration.get_by_id")
def test_unregister_self_valid(mock_get_by_id):
    # DADO um usuário comum
    actor = Mock()
    actor.has_perm.return_value = False

    # E DADO um registration type
    registration_type = Mock()

    # E DADO que existe uma registration do usuário nesse type
    registration = Mock()
    registration.registration_type = registration_type
    registration.user = actor
    mock_get_by_id.return_value = registration

    # QUANDO remover a registration
    event_registration_service.unregister(actor=actor, event_registration_id=1)

    # ENTÃO o ORM deve ser chamado
    assert registration.delete.call_count == 1


@mock.patch("eventos2.core.services.event_registration.get_by_id")
def test_unregister_other_user_valid(mock_get_by_id):
    # DADO um usuário que tem permissões
    actor = Mock()
    actor.has_perm.return_value = True

    # E DADO outro usuário alvo
    target = Mock()

    # E DADO um registration type
    registration_type = Mock()

    # E DADO que existe uma registration do usuário alvo nesse type
    registration = Mock()
    registration.registration_type = registration_type
    registration.user = target
    mock_get_by_id.return_value = registration

    # QUANDO o actor remover a registration do usuário alvo
    event_registration_service.unregister(actor=actor, event_registration_id=1)

    # ENTÃO o ORM deve ser chamado
    assert registration.delete.call_count == 1


@mock.patch("eventos2.core.services.event_registration.get_by_id")
def test_unregister_other_user_unauthorized(mock_get_by_id):
    # DADO um usuário comum
    actor = Mock()
    actor.has_perm.return_value = False

    # E DADO um usuário alvo
    target = Mock()

    # E DADO um registration type
    registration_type = Mock()

    # E DADO que existe uma registration do usuário alvo nesse type
    registration = Mock()
    registration.registration_type = registration_type
    registration.user = target
    mock_get_by_id.return_value = registration

    # QUANDO o actor tentar remover a registration do usuário alvo
    # ENTÃO o serviço deve gerar sua exceção de falta de permissões
    with pytest.raises(NotAuthorizedError):
        event_registration_service.unregister(actor=actor, event_registration_id=1)


@mock.patch("eventos2.core.services.event_registration.EventRegistration")
def test_find_by_user_valid(mock_registration):
    # DADO um usuário comum
    actor = Mock()

    # E DADO que o banco retorna uma registration
    expected_registrations = Mock()
    mock_registration.objects.filter.return_value = expected_registrations

    # QUANDO o usuário listar seus registrations
    registrations = event_registration_service.find_by_user(actor=actor, user=actor)

    # ENTÃO as registrations devem ser retornadas
    assert registrations is expected_registrations


@mock.patch("eventos2.core.services.event_registration.EventRegistration")
def test_find_by_user_unauthorized(mock_registration):
    # DADO um usuário comum
    actor = Mock()
    # E DADO um outro usuário alvo
    target = Mock()

    # QUANDO o ator listar as registrations do usuário alvo
    # ENTÃO o serviço deverá gerar sua exceção de falta de permissões
    with pytest.raises(NotAuthorizedError):
        event_registration_service.find_by_user(actor=actor, user=target)


@mock.patch("eventos2.core.services.event_registration.EventRegistration")
def test_find_by_user_and_event_valid(mock_registration):
    # DADO um usuário comum
    actor = Mock()

    # E DADO que o banco retorna uma registration
    expected_registrations = Mock()
    mock_registration.objects.filter.return_value = expected_registrations

    # E DADO um evento
    event = Mock()

    # QUANDO o usuário listar seus registrations
    registrations = event_registration_service.find_by_user_and_event(
        actor=actor, user=actor, event=event
    )

    # ENTÃO as registrations devem ser retornadas
    assert registrations is expected_registrations


@mock.patch("eventos2.core.services.event_registration.EventRegistration")
def test_find_by_user_and_event_unauthorized(mock_registration):
    # DADO um usuário comum
    actor = Mock()
    # E DADO um outro usuário alvo
    target = Mock()
    # E DADO um evento
    event = Mock()

    # QUANDO o ator listar as registrations do usuário alvo
    # ENTÃO o serviço deverá gerar sua exceção de falta de permissões
    with pytest.raises(NotAuthorizedError):
        event_registration_service.find_by_user_and_event(
            actor=actor, user=target, event=event
        )
