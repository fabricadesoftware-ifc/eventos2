import rules


@rules.predicate
def is_event_owner(user, event):
    return event and event.owners.filter(pk=user.pk).exists()


@rules.predicate
def is_registered_to_event(user, obj):
    event = getattr(obj, "event", obj)
    return (
        user.is_authenticated
        and event
        and event.registrations.filter(user=user).exists()
    )


@rules.predicate
def user_is_self(user, target_user):
    return user.pk == target_user.pk
