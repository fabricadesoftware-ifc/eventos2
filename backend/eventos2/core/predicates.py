import rules


@rules.predicate
def is_event_owner(user, event):
    return event and event.owners.filter(pk=user.pk).exists()
