from unittest import mock
from unittest.mock import Mock

import pytest
from django.utils import timezone

from eventos2.core.services import event as event_service
from eventos2.utils.exceptions import (
    DuplicateIdentifierError,
    NotAuthorizedError,
    NotFoundError,
)


@mock.patch("eventos2.core.services.event.Event")
def test_get_by_id_valid(mock_event):
    # DADO que o banco retorna um evento
    expected_event = Mock()
    mock_event.available_objects.get.return_value = expected_event

    # QUANDO obter um evento com um ID qualquer
    event = event_service.get_by_id(123)

    # ENTÃO o banco deve ser consultado com esse ID
    assert mock_event.available_objects.get.call_args == mock.call(pk=123)
    # E ENTÃO o evento retornado deve ser o mesmo que o ORM retornou
    assert event is expected_event


@mock.patch("eventos2.core.services.event.Event")
def test_get_by_id_invalid(mock_event):
    # DADO que o banco não retorna um evento (gera exceção)
    mock_event.DoesNotExist = Exception
    mock_event.available_objects.get.side_effect = mock_event.DoesNotExist

    # QUANDO tentar obter um evento com um ID qualquer
    # ENTÃO o serviço deve gerar sua própria exceção
    with pytest.raises(NotFoundError):
        event_service.get_by_id(123)


@mock.patch("eventos2.core.services.event.Event")
def test_get_by_slug_valid(mock_event):
    # DADO que o banco retorna um evento
    expected_event = Mock()
    mock_event.available_objects.get.return_value = expected_event

    # QUANDO tentar obter um evento com um slug qualquer
    event = event_service.get_by_slug("event-a")

    # ENTÃO o banco deve ser consultado com esse slug
    assert mock_event.available_objects.get.call_args == mock.call(slug="event-a")
    # E ENTÃO o evento retornado deve ser o mesmo que o ORM retornou
    assert event is expected_event


@mock.patch("eventos2.core.services.event.Event")
def test_get_by_slug_invalid(mock_event):
    # DADO que o banco não retorna um evento (gera exceção)
    mock_event.DoesNotExist = Exception
    mock_event.available_objects.get.side_effect = mock_event.DoesNotExist

    # QUANDO tentar obter um evento com um slug qualquer
    # ENTÃO o serviço deve gerar sua própria exceção
    with pytest.raises(NotFoundError):
        event_service.get_by_slug("event-a")


@mock.patch("eventos2.core.services.event.Event")
def test_exists_by_slug_valid(mock_event):
    # DADO que o banco afirma que a toda consulta tem resultados
    mock_event.available_objects.filter.return_value = mock_event.available_objects
    mock_event.available_objects.exists.return_value = True

    # QUANDO verificar se existe um evento com uma slug qualquer
    # ENTÃO o serviço deve afirmar que sim
    assert event_service.exists_by_slug("event-a") is True


@mock.patch("eventos2.core.services.event.Event")
def test_exists_by_slug_invalid(mock_event):
    # DADO que o banco afirma que a toda consulta não tem resultados
    mock_event.available_objects.filter.return_value = mock_event.available_objects
    mock_event.available_objects.exists.return_value = False

    # QUANDO verificar se existe um evento com uma slug qualquer
    # ENTÃO o serviço deve afirmar que não
    assert event_service.exists_by_slug("event-a") is False


@mock.patch("eventos2.core.services.event.Event")
@mock.patch("eventos2.core.services.event.exists_by_slug")
def test_create_valid(mock_exists_by_slug, mock_event):
    # DADO que o banco aceita criar qualquer evento, e o retorna
    expected_event = Mock()
    mock_event.objects.create.return_value = expected_event

    # E DADO que não há eventos que causem colisões de slug
    mock_exists_by_slug.return_value = False

    # E DADO um usuário que tem permissões
    actor = Mock()
    actor.has_perm.return_value = True

    # QUANDO criar um evento
    event = event_service.create(
        actor=actor,
        slug="event-a",
        name="Event A",
        starts_on=timezone.now,
        ends_on=timezone.now(),
    )

    # ENTÃO o ORM deve ser chamado para criar o evento
    assert mock_event.objects.create.call_count == 1

    # E ENTÃO o usuário criador deve ser adicionado como dono do evento
    assert event.owners.add.call_count == 1
    assert event.owners.add.call_args == mock.call(actor)

    # E ENTÃO o evento deve ser retornado
    assert event is expected_event


@mock.patch("eventos2.core.services.event.Event")
def test_create_unauthorized(mock_event):
    # DADO um usuário que não tem permissão alguma
    actor = Mock()
    actor.has_perm.return_value = False

    # QUANDO tentar criar um evento
    # ENTÃO o serviço deverá gerar sua exeção de falta de permissões
    with pytest.raises(NotAuthorizedError):
        event_service.create(
            actor=actor,
            slug="event-a",
            name="Event A",
            starts_on=timezone.now,
            ends_on=timezone.now(),
        )


@mock.patch("eventos2.core.services.event.exists_by_slug")
def test_create_duplicate_slug(mock_exists_by_slug):
    # DADO que haverá uma colisão de slugs
    # (já existe um evento com a slug escolhida)
    mock_exists_by_slug.return_value = True

    # E DADO um usuário que tem permissões
    actor = Mock()
    actor.has_perm.return_value = True

    # QUANDO tentar criar um evento
    # ENTÃO o serviço deve gerar sua exceção de colisão de slugs
    with pytest.raises(DuplicateIdentifierError):
        event_service.create(
            actor=actor,
            slug="event-a",
            name="Event A",
            starts_on=timezone.now,
            ends_on=timezone.now(),
        )


@mock.patch("eventos2.core.services.event.get_by_id")
@mock.patch("eventos2.core.services.event.exists_by_slug")
def test_update_valid_new_slug(mock_exists_by_slug, mock_get_by_id):
    # DADO que o evento a ser editado existe
    event = Mock()
    mock_get_by_id.return_value = event

    # E DADO um usuário que tem permissões
    actor = Mock()
    actor.has_perm.return_value = True

    # E DADO que não haverá colisão de slugs com outro evento
    mock_exists_by_slug.return_value = False

    # QUADO editar o evento
    event_service.update(
        actor=actor,
        event_id=123,
        slug="new slug",
        name="Event A",
        starts_on=timezone.now(),
        ends_on=timezone.now(),
    )

    # ENTÃO o evento deve ser obtido
    assert mock_get_by_id.call_count == 1
    assert mock_get_by_id.call_args == mock.call(123)

    # E ENTÃO o evento deve ser modificado e salvo
    assert event.slug == "new slug"
    assert event.save.call_count == 1


@mock.patch("eventos2.core.services.event.get_by_id")
@mock.patch("eventos2.core.services.event.get_by_slug")
@mock.patch("eventos2.core.services.event.exists_by_slug")
def test_update_valid_keep_slug(mock_exists_by_slug, mock_get_by_slug, mock_get_by_id):
    # DADO que o evento a ser editado existe
    event = Mock()
    mock_get_by_id.return_value = event

    # E DADO um usuário que tem permissões
    actor = Mock()
    actor.has_perm.return_value = True

    # E DADO que não haverá colisão de slugs,
    # pois o evento existente manterá sua slug.
    mock_exists_by_slug.return_value = True
    mock_get_by_slug.return_value = event

    # QUANDO editar o evento mantendo a slug anterior
    event_service.update(
        actor=actor,
        event_id=1,
        slug="same slug as before",
        name="new name",
        starts_on=timezone.now(),
        ends_on=timezone.now(),
    )

    # ENTÃO o evento deve ser modificado e salvo.
    assert event.slug == "same slug as before"
    assert event.name == "new name"
    assert event.save.call_count == 1


@mock.patch("eventos2.core.services.event.get_by_id")
@mock.patch("eventos2.core.services.event.get_by_slug")
@mock.patch("eventos2.core.services.event.exists_by_slug")
def test_update_duplicate_slug(mock_exists_by_slug, mock_get_by_slug, mock_get_by_id):
    # DADO que o evento a ser editado existe
    event_to_be_edited = Mock()
    mock_get_by_id.return_value = event_to_be_edited

    # E DADO um usuário que tem permissões
    actor = Mock()
    actor.has_perm.return_value = True

    # E DADO outro evento existente já usando a nova slug
    existing_event = Mock()
    mock_exists_by_slug.return_value = True
    mock_get_by_slug.return_value = existing_event

    # QUANDO tentar editar o evento
    # ENTÃO o serviço deve gerar sua exceção de colisão de slugs
    with pytest.raises(DuplicateIdentifierError):
        event_service.update(
            actor=actor,
            event_id=1,
            slug="some slug",
            name="some name",
            starts_on=timezone.now(),
            ends_on=timezone.now(),
        )


@mock.patch("eventos2.core.services.event.get_by_id")
def test_update_unauthorized(mock_get_by_id):
    # DADO que o evento a ser editado existe
    event = Mock()
    mock_get_by_id.return_value = event

    # E DADO um usuário que não tem permissão alguma
    actor = Mock()
    actor.has_perm.return_value = False

    # QUANDO tentar editar o evento
    # ENTÃO o serviço deve gerar sua exceção de falta de permissões
    with pytest.raises(NotAuthorizedError):
        event_service.update(
            actor=actor,
            event_id=123,
            slug="new slug",
            name="Event A",
            starts_on=timezone.now(),
            ends_on=timezone.now(),
        )


@mock.patch("eventos2.core.services.event.get_by_id")
def test_delete_valid(mock_get_by_id):
    # DADO que o evento a ser deletado existe
    event = Mock()
    mock_get_by_id.return_value = event

    # E DADO um usuário que tem permissões
    actor = Mock()
    actor.has_perm.return_value = True

    # QUANDO deletar o evento
    event_service.delete(actor=actor, event_id=1)

    # ENTÃO o ORM deve ser chamado
    assert event.delete.call_count == 1


@mock.patch("eventos2.core.services.event.get_by_id")
def test_delete_unauthorized(mock_get_by_id):
    # DADO que o evento a ser deletado existe
    event = Mock()
    mock_get_by_id.return_value = event

    # E DADO um usuário que não tem permissão alguma
    actor = Mock()
    actor.has_perm.return_value = False

    # QUANDO tentar deletar o evento
    # ENTÃO o serviço deve gerar sua exceção de falta de permissões
    with pytest.raises(NotAuthorizedError):
        event_service.delete(actor=actor, event_id=1)


@mock.patch("eventos2.core.services.event.EventRegistration")
@mock.patch("eventos2.core.services.event.get_by_id")
def test_find_registrations_valid(mock_get_by_id, mock_eventregistration):
    # DADO um evento
    event = Mock()
    mock_get_by_id.return_value = event

    # E DADO um usuário que tem permissões
    actor = Mock()
    actor.has_perm.return_value = True

    # E DADO que o banco retorna inscrições
    expected_registrations = Mock()
    mock_eventregistration.objects.filter.return_value = expected_registrations

    # QUANDO listar as inscrições do evento
    registrations = event_service.find_registrations(actor=actor, event_id=1)

    # ENTÃO as inscrições serão retornadas
    assert registrations is expected_registrations


@mock.patch("eventos2.core.services.event.get_by_id")
def test_find_registrations_unauthorized(mock_get_by_id):
    # DADO um evento
    event = Mock()
    mock_get_by_id.return_value = event

    # E DADO um usuário que não tem permissão alguma
    actor = Mock()
    actor.has_perm.return_value = False

    # QUANDO tentar listar as inscrições o evento
    # ENTÃO o serviço deve gerar sua exceção de falta de permissões
    with pytest.raises(NotAuthorizedError):
        event_service.find_registrations(actor=actor, event_id=1)
