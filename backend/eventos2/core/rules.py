import rules

from eventos2.core import predicates

rules.add_perm("core.change_event", predicates.is_event_owner)
rules.add_perm("core.delete_event", predicates.is_event_owner)
rules.add_perm("core.view_registrations_for_event", predicates.is_event_owner)
