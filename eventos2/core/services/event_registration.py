from eventos2.core.models import Event, EventRegistration, User
from eventos2.utils.exceptions import ConflictError, NotAuthorizedError, NotFoundError


def get_by_id(event_registration_id: int) -> EventRegistration:
    try:
        registration = EventRegistration.objects.get(pk=event_registration_id)
    except EventRegistration.DoesNotExist:
        raise NotFoundError("Event registration not found.")
    return registration


def exists_by_event_and_user(event: Event, user: User) -> bool:
    return EventRegistration.objects.filter(event=event, user=user).exists()


def register(
    *, actor: User, event: Event, user: User
) -> EventRegistration:
    is_self_registering = actor == user
    cannot_self_register = not actor.has_perm(
        "core.register_self_into_event", event
    )
    cannot_register_anyone = not actor.has_perm(
        "core.change_event", event
    )

    if is_self_registering and cannot_self_register and cannot_register_anyone:
        raise NotAuthorizedError(
            "You're not authorized to self register into this event."
        )
    elif not is_self_registering and cannot_register_anyone:
        raise NotAuthorizedError(
            "You're not authorized to register an user into this event."
        )

    if exists_by_event_and_user(event, user):
        raise ConflictError("This registration already exists.")

    registration = EventRegistration.objects.create(
        event=event, user=user
    )
    return registration


def unregister(*, actor: User, event_registration_id: int) -> None:
    registration = get_by_id(event_registration_id)

    is_self_unregistering = actor == registration.user
    can_unregister_anyone = actor.has_perm(
        "core.change_event", registration.event
    )

    if not (is_self_unregistering or can_unregister_anyone):
        raise NotAuthorizedError("You're not authorized remove this registration.")

    registration.delete()


def find_by_user(*, actor: User, user: User):
    if actor != user:
        raise NotAuthorizedError(
            "You're not authorized to view these event registrations."
        )

    return EventRegistration.objects.filter(user=user)


def find_by_user_and_event(*, actor: User, user: User, event: Event):
    if actor != user:
        raise NotAuthorizedError(
            "You're not authorized to view these event registrations."
        )

    return EventRegistration.objects.filter(user=user, event=event)
