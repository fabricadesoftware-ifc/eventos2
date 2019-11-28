from datetime import datetime

from eventos2.core.models import Event, EventRegistration, User
from eventos2.images.models import Image
from eventos2.utils.exceptions import (
    DuplicateIdentifierError,
    NotAuthorizedError,
    NotFoundError,
)


def get_by_id(event_id: int) -> Event:
    try:
        event = Event.available_objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise NotFoundError("Event not found")

    return event


def create(
    *,
    actor: User,
    slug: str,
    name: str,
    name_english: str = None,
    starts_on: datetime,
    ends_on: datetime,
    logo: Image = None
) -> Event:
    if not actor.has_perm("core.add_event"):
        raise NotAuthorizedError("Not authorized to create an event.")

    slug_is_taken = Event.objects.filter(slug=slug).exists()
    if slug_is_taken:
        raise DuplicateIdentifierError("Slug already used.")

    event = Event.objects.create(
        slug=slug,
        name=name,
        name_english=name_english or "",
        starts_on=starts_on,
        ends_on=ends_on,
        logo=logo,
    )
    event.owners.add(actor)
    return event


def update(
    *,
    actor: User,
    event_id: int,
    slug: str,
    name: str,
    name_english: str = None,
    starts_on: datetime,
    ends_on: datetime,
    logo: Image = None
) -> Event:
    event = get_by_id(event_id)

    if not actor.has_perm("core.change_event", event):
        raise NotAuthorizedError("Not authorized to edit this event.")

    event_pks_using_slug = (
        Event.objects.filter(slug=slug).values_list("pk", flat=True).first()
    )
    if event_pks_using_slug is not None and event_pks_using_slug != event.pk:
        raise DuplicateIdentifierError("Slug already used.")

    event.slug = slug
    event.name = name
    event.name_english = name_english or ""
    event.starts_on = starts_on
    event.ends_on = ends_on
    event.logo = logo
    event.save()
    return event


def delete(*, actor: User, event_id: int) -> None:
    event = get_by_id(event_id)

    if not actor.has_perm("core.delete_event", event):
        raise NotAuthorizedError("Not authorized to delete this event.")

    event.delete()


def find_registrations(*, actor: User, event_id: int) -> None:
    event = get_by_id(event_id)

    if not actor.has_perm("core.view_registrations_for_event", event):
        raise NotAuthorizedError("Not authorized to view registrations for this event")

    return EventRegistration.objects.filter(registration_type__event=event)
