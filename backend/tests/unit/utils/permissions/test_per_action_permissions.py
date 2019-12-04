from unittest.mock import Mock

import pytest

from eventos2.utils.permissions import PerActionPermissions


def create_mock_user(*, is_authenticated, permissions=None):
    """
    Cria um mock de usuário com as permissões dadas.
    """
    user = Mock()
    user.is_authenticated = is_authenticated
    user.user_permissions.all.return_value = permissions or []
    user.has_perms = lambda perms: all(
        perm in user.user_permissions.all() for perm in perms
    )
    return user


def test_authenticated_user():
    instance = PerActionPermissions()

    request = Mock()
    request.user = create_mock_user(
        is_authenticated=True, permissions=["applabel.change_dog"]
    )

    view = Mock()
    view.per_action_permissions = {
        "create": PerActionPermissions.ALLOW_AUTHENTICATED,
        "retrieve": PerActionPermissions.ALLOW_ANY,
        "update": ["applabel.change_dog"],
        "destroy": ["applabel.delete_dog"],
    }

    # Permissão deve ser concedida, pois o usuário está autenticado.
    view.action = "create"
    assert instance.has_permission(request, view) is True

    # Permissão deve ser concedida, pois a action está liberada para todos.
    view.action = "retrieve"
    assert instance.has_permission(request, view) is True

    # Permissão deve ser concedida, pois o usuário tem a permissão requerida.
    view.action = "update"
    assert instance.has_permission(request, view) is True

    # Permissão não deve ser concecida, pois o usuário não tem a permissão requrida.
    view.action = "destroy"
    assert instance.has_permission(request, view) is False


def test_unauthenticated_user():
    instance = PerActionPermissions()

    request = Mock()
    request.user = create_mock_user(is_authenticated=False)

    view = Mock()
    view.per_action_permissions = {
        "create": PerActionPermissions.ALLOW_AUTHENTICATED,
        "retrieve": PerActionPermissions.ALLOW_ANY,
        "update": ["applabel.change_dog"],
        "destroy": ["applabel.delete_dog"],
    }

    # Permissão não deve ser concedida, pois o usuário não está autenticado.
    view.action = "create"
    assert instance.has_permission(request, view) is False

    # Permissão deve ser concedida, pois a action está liberada para todos.
    view.action = "retrieve"
    assert instance.has_permission(request, view) is True

    # Permissão não deve ser concedida, pois o usuário não está autenticado
    # e então não pode ter a permissão requerida.
    view.action = "update"
    assert instance.has_permission(request, view) is False

    # Permissão não deve ser concedida, pois o usuário não está autenticado
    # e então não pode ter a permissão requerida.
    view.action = "destroy"
    assert instance.has_permission(request, view) is False


def test_authenticated_user_object_level_permissions():
    instance = PerActionPermissions()

    user_permissions = ["applabel.add_dog"]
    dog_owned_by_user = object()
    dog_not_owned_by_user = object()

    request = Mock()
    request.user = Mock()
    request.user.is_authenticated = True
    request.user.user_permissions.all.return_value = user_permissions
    request.user.has_perms = lambda perms, obj=None: all(
        (
            perm in request.user.user_permissions.all()
            and (obj is None or obj is dog_owned_by_user)
        )
        for perm in perms
    )

    view = Mock()
    view.per_action_permissions = {
        "create": ["applabel.add_dog"],
        "retrieve": PerActionPermissions.ALLOW_ANY,
        "update": ["applabel.change_dog"],
        "delete": PerActionPermissions.DENY_ALL,
    }

    view.action = "create"
    # Permissão deve ser concedida,
    # pois o usuário tem a permissão requerida.
    assert instance.has_permission(request, view) is True
    # Permissão deve ser concedida,
    # pois o usuário tem a permissão requerida para este objeto.
    assert instance.has_object_permission(request, view, dog_owned_by_user) is True
    # Permissão não deve ser concedida,
    # pois o usuário não tem a permissão requerida para este objeto.
    assert instance.has_object_permission(request, view, dog_not_owned_by_user) is False

    view.action = "retrieve"
    # Permissão deve ser concedida,
    # pois a action está aberta para todos.
    assert instance.has_permission(request, view) is True
    assert instance.has_object_permission(request, view, dog_owned_by_user) is True
    assert instance.has_object_permission(request, view, dog_not_owned_by_user) is True

    view.action = "update"
    # Permissão não deve ser concedida,
    # pois o usuário não tem a permissão requerida para nenhum objeto.
    assert instance.has_permission(request, view) is False
    assert instance.has_object_permission(request, view, dog_owned_by_user) is False
    assert instance.has_object_permission(request, view, dog_not_owned_by_user) is False

    view.action = "delete"
    # Permissão não deve ser concedida,
    # pois a action está bloqueada para todos.
    assert instance.has_permission(request, view) is False
    assert instance.has_object_permission(request, view, dog_owned_by_user) is False
    assert instance.has_object_permission(request, view, dog_not_owned_by_user) is False


def test_invalid_action():
    instance = PerActionPermissions()

    request = Mock()
    request.user = create_mock_user(is_authenticated=False)

    view = Mock()
    view.per_action_permissions = {
        "create": PerActionPermissions.ALLOW_AUTHENTICATED,
        "retrieve": PerActionPermissions.ALLOW_AUTHENTICATED,
        "update": PerActionPermissions.ALLOW_AUTHENTICATED,
        "destroy": PerActionPermissions.ALLOW_AUTHENTICATED,
    }

    # Permissão não deve ser concecida, pois a ação não foi determinada.
    del view.action
    assert instance.has_permission(request, view) is False

    # Permissão não deve ser concecida, pois a ação não foi determinada.
    view.action = None
    assert instance.has_permission(request, view) is False

    # Permissão não deve ser concecida, pois a ação não está presente no
    # `per_action_permissions`.
    view.action = "some_other_action"
    assert instance.has_permission(request, view) is False


def test_metadata_action():
    instance = PerActionPermissions()

    request = Mock()
    request.user = create_mock_user(is_authenticated=False)

    view = Mock()
    view.per_action_permissions = {
        "create": PerActionPermissions.ALLOW_AUTHENTICATED,
        "retrieve": PerActionPermissions.ALLOW_AUTHENTICATED,
        "update": PerActionPermissions.ALLOW_AUTHENTICATED,
        "destroy": PerActionPermissions.ALLOW_AUTHENTICATED,
    }

    # Permissão deve ser concecida, pois a ação indica um request do tipo
    # OPTIONS, essencial para o funcionamento do CORS.
    view.action = "metadata"
    assert instance.has_permission(request, view) is True


def test_permission_mapping_not_defined():
    instance = PerActionPermissions()

    request = Mock()
    view = Mock()
    del view.per_action_permissions

    # Uma exeção deve ser gerada, pois a view não tem o mapeamento de ações
    # para permissões definido.
    with pytest.raises(TypeError):
        instance.has_permission(request, view)
