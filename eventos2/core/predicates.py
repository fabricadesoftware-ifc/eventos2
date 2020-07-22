import rules


@rules.predicate
def is_event_owner(user, obj):
    event = getattr(obj, "event", obj)
    return event and event.owners.filter(pk=user.pk).exists()


@rules.predicate
def is_submission_author(user, obj):
    submission = getattr(obj, "submission", obj)
    return submission and submission.authors.filter(pk=user.pk).exists()


@rules.predicate
def is_registered_to_event(user, obj):
    event = getattr(obj, "event", obj)
    return (
        user.is_authenticated
        and event
        and event.registrations.filter(user=user).exists()
    )
