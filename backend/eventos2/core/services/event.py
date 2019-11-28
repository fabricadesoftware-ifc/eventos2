from datetime import datetime

from eventos2.core.models import Event, EventRegistration
from eventos2.images.models import Image
from eventos2.utils.exceptions import DuplicateIdentifierError, NotFoundError


def get_by_id(event_id: int) -> Event:
    try:
        return Event.available_objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise NotFoundError("Event not found")


def create(
    *,
    slug: str,
    name: str,
    name_english: str = None,
    starts_on: datetime,
    ends_on: datetime,
    logo: Image = None
) -> Event:
    slug_is_taken = Event.objects.filter(slug=slug).exists()
    if slug_is_taken:
        raise DuplicateIdentifierError("Slug already used.")

    return Event.objects.create(
        slug=slug,
        name=name,
        name_english=name_english or "",
        starts_on=starts_on,
        ends_on=ends_on,
        logo=logo,
    )


def update(
    event_id: int,
    *,
    slug: str,
    name: str,
    name_english: str = None,
    starts_on: datetime,
    ends_on: datetime,
    logo: Image = None
) -> Event:
    event = get_by_id(event_id)

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


def delete(event_id: int) -> None:
    event = get_by_id(event_id)
    event.delete()


def find_registrations(event_id: int) -> None:
    event = get_by_id(event_id)
    return EventRegistration.objects.filter(registration_type__event=event)
