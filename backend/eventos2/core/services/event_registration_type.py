from typing import Any, Optional

from django.db.models.deletion import ProtectedError

from eventos2.core.models import Event, EventRegistration, EventRegistrationType, User
from eventos2.utils.exceptions import ConflictError, NotAuthorizedError, NotFoundError


def get_by_id(event_registration_type_id: int) -> EventRegistrationType:
    try:
        registration_type = EventRegistrationType.objects.get(
            pk=event_registration_type_id
        )
    except EventRegistrationType.DoesNotExist:
        raise NotFoundError("Event registration type not found")

    return registration_type


def create(
    *, actor: User, event: Event, name: str, name_english: Optional[str] = None
) -> EventRegistrationType:
    if not actor.has_perm("core.change_event", event):
        raise NotAuthorizedError(
            "Not authorized to add a registration type to this event."
        )

    registration_type = EventRegistrationType.objects.create(
        event=event, name=name, name_english=name_english or ""
    )
    return registration_type


def update(
    *,
    actor: User,
    event_registration_type_id: int,
    name: str,
    name_english: Optional[str] = None
) -> EventRegistrationType:
    registration_type = get_by_id(event_registration_type_id)

    if not actor.has_perm("core.change_event", registration_type.event):
        raise NotAuthorizedError(
            "Not authorized to edit a registration type in this event."
        )

    registration_type.name = name
    registration_type.name_english = name_english or ""
    registration_type.save()
    return registration_type


def delete(*, actor: User, event_registration_type_id: int) -> None:
    registration_type = get_by_id(event_registration_type_id)

    if not actor.has_perm("core.change_event", registration_type.event):
        raise NotAuthorizedError(
            "Not authorized to remove a registration type in this event."
        )

    try:
        registration_type.delete()
    except ProtectedError:
        raise ConflictError(
            "This registration type cannot be deleted"
            " because it already has registrations."
        )


def find_registrations(*, actor: User, event_registration_type_id: int) -> Any:
    registration_type = get_by_id(event_registration_type_id)

    if not actor.has_perm("core.view_registrations_for_event", registration_type.event):
        raise NotAuthorizedError("Not authorized to view registrations for this event")

    return EventRegistration.objects.filter(registration_type=registration_type)
