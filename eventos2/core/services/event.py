from datetime import datetime
from typing import Any, Optional

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


def get_by_slug(slug: str) -> Event:
    try:
        event = Event.available_objects.get(slug=slug)
    except Event.DoesNotExist:
        raise NotFoundError("Event not found")

    return event


def exists_by_slug(slug: str) -> bool:
    return Event.available_objects.filter(slug=slug).exists()


def create(
    *,
    actor: User,
    slug: str,
    name: str,
    name_english: Optional[str] = None,
    starts_on: datetime,
    ends_on: datetime,
    logo: Optional[Image] = None
) -> Event:
    if not actor.has_perm("core.add_event"):
        raise NotAuthorizedError("Not authorized to create an event.")

    if exists_by_slug(slug):
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
    name_english: Optional[str] = None,
    starts_on: datetime,
    ends_on: datetime,
    logo: Optional[Image] = None
) -> Event:
    event = get_by_id(event_id)

    if not actor.has_perm("core.change_event", event):
        raise NotAuthorizedError("Not authorized to edit this event.")

    if exists_by_slug(slug) and get_by_slug(slug) != event:
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


def find_registrations(*, actor: User, event_id: int) -> Any:
    event = get_by_id(event_id)

    if not actor.has_perm("core.view_registrations_for_event", event):
        raise NotAuthorizedError("Not authorized to view registrations for this event")

    return EventRegistration.objects.filter(event=event)
