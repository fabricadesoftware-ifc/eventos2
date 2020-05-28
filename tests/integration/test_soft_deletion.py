import pytest

from eventos2.core.models import Event


@pytest.mark.django_db
def test_hard_deletion(event_factory):
    event_factory(slug="event-a", owners=[]).hard_delete()
    assert not Event.objects.filter(slug="event-a").exists()


@pytest.mark.django_db
def test_soft_deletion(event_factory):
    event_factory(slug="event-a", owners=[]).delete()
    event_factory(slug="event-b", owners=[])

    assert Event.objects.get(slug="event-a")
    assert Event.objects.get(slug="event-a").deleted_on is not None
    assert not Event.available_objects.filter(slug="event-a").exists()

    assert Event.objects.get(slug="event-b").deleted_on is None
    assert Event.available_objects.filter(slug="event-b").exists()


@pytest.mark.django_db
def test_soft_undeletion(event_factory):
    event_a = event_factory(slug="event-a", owners=[])

    event_a.delete()
    assert Event.objects.get(slug="event-a").deleted_on is not None

    event_a.undelete()
    assert Event.objects.get(slug="event-a").deleted_on is None


@pytest.mark.django_db
def test_soft_deletion_queryset(event_factory):
    event_factory(slug="event-a", owners=[])
    event_factory(slug="event-b", owners=[])
    event_factory(slug="event-c", owners=[])

    Event.objects.delete()
    assert all(x.deleted_on is not None for x in Event.objects.all())
    assert not Event.available_objects.exists()

    Event.objects.undelete()
    assert all(x.deleted_on is None for x in Event.objects.all())
    assert Event.available_objects.count() == 3

    Event.objects.hard_delete()
    assert not Event.objects.exists()
