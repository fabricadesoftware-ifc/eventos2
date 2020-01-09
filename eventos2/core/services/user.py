from eventos2.core.models import User
from eventos2.utils.exceptions import (
    DuplicateIdentifierError,
    NotAuthorizedError,
    NotFoundError,
)


def get_by_id(user_id: int, *, must_be_active: bool = False) -> User:
    queryset = User.objects
    if must_be_active:
        queryset = queryset.filter(is_active=True)

    try:
        user = queryset.get(pk=user_id)
    except User.DoesNotExist:
        raise NotFoundError("User not found.")
    return user


def exists_by_email(email: str) -> bool:
    return User.objects.filter(email=email).exists()


def create(*, email: str, password: str, first_name: str, last_name: str) -> User:
    if exists_by_email(email):
        raise DuplicateIdentifierError("Email already used.")

    user = User.objects.create(
        email=email, username=email, first_name=first_name, last_name=last_name
    )
    user.set_password(password)
    user.save()

    return user


def update(*, actor: User, user_id: int, first_name: str, last_name: str) -> User:
    user = get_by_id(user_id)

    if not actor.has_perm("core.change_user", user):
        raise NotAuthorizedError("Not authorized to edit this user.")

    user.first_name = first_name
    user.last_name = last_name
    user.save()

    return user


def delete(*, actor: User, user_id: int) -> None:
    user = get_by_id(user_id)

    if not actor.has_perm("core.delete_user", user):
        raise NotAuthorizedError("Not authorized to delete this user.")

    user.delete()
