import warnings

from rest_framework.permissions import BasePermission


class PerActionPermissions(BasePermission):
    """
    Autentica o request usando permissões à nivel de objeto.
    Requer um backend com suporte a isso, como o django-rules.

    As permissões requeridas são configuráveis por meio do atributo
    `per_action_permissions`, que deve ser setado no ViewSet.
    Deve conter um dicionário, mapeando ações (list, retrieve)
    a listas de permissões do Django.

    Essas constantes podem ser utilizadas em vez da lista:

    * `ALLOW_AUTHENTICATED`: Permitir apenas usuários autenticados.
                             Equivalente a uma lista vazia.
    * `ALLOW_ANY`: Permitir tudo mundo, até usuários não autenticados.
    * `DENY_ALL`: Permitir ninguém. Geralmente não é util.

    Requests pre-flight com o método OPTIONS (CORS), que têm a ação "metadata",
    sempre são permitidos.

    Ações não definidas em `per_action_permissions` são sempre bloqueadas.

    Exemplo:

    ```
    class DogViewSet(ModelViewSet):
        permission_classes = [PerActionPermissions]
        per_action_permissions = {
            'create': ['appname.add_dog'],
            'destroy': ['appname.delete_dog'],
            'list': PerActionPermissions.ALLOW_AUTHENTICATED,
            'retrieve': PerActionPermissions.ALLOW_ANY,
            'update': ['appname.change_dog'],
        }
    ```
    """

    ALLOW_AUTHENTICATED = []
    ALLOW_ANY = object()  # valor único
    DENY_ALL = object()

    def get_action(self, view):
        if hasattr(view, "action"):
            return view.action

        warnings.warn(
            "PerActionPermissions could not find an action."
            " It only works in ViewSets. Is it being used in one?"
        )
        return None

    def get_permissions_map(self, view):
        if not hasattr(view, "per_action_permissions"):
            raise TypeError(
                "The `per_action_permissions` attribute must be set"
                " in the ViewSet when using the PerActionPermimissions class."
            )
        return view.per_action_permissions

    def get_required_permissions(self, view):
        """
        Determina quais permissões devem ser verificadas para a view
        e sua action atual, usando o atributo `per_action_permissions`.
        """

        action = self.get_action(view)
        if action is None:
            # A ação não foi especificada. Bloquear.
            return self.DENY_ALL
        if action == "metadata":
            # É um request OPTIONS. Sempre permitir.
            return self.ALLOW_ANY

        perms_map = self.get_permissions_map(view)
        if action not in perms_map:
            # A ação não foi especificada em `per_action_permissions`. Bloquear.
            return self.DENY_ALL

        return perms_map[action]

    def has_permission(self, request, view):
        """
        Returns `True` if permission is granted, `False` otherwise.
        """
        perms = self.get_required_permissions(view)

        if perms is self.ALLOW_ANY:
            return True
        elif perms is self.DENY_ALL:
            return False

        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.has_perms(perms)

    def has_object_permission(self, request, view, obj):
        """
        Returns `True` if permission is granted, `False` otherwise.
        """
        # authentication checks have already executed via has_permission
        perms = self.get_required_permissions(view)
        if perms is self.ALLOW_ANY:
            return True
        elif perms is self.DENY_ALL:
            return False

        return request.user.has_perms(perms, obj)
