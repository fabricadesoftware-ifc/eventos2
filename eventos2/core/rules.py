import rules

from eventos2.core import predicates

rules.add_perm("core.change_event", predicates.is_event_owner)
rules.add_perm("core.delete_event", predicates.is_event_owner)
rules.add_perm("core.answer_review", predicates.is_review_author)
rules.add_perm("core.view_activities_for_event", rules.is_authenticated)
rules.add_perm("core.view_registrations_for_event", predicates.is_event_owner)
rules.add_perm("core.view_submissions_for_event", predicates.is_event_owner)
rules.add_perm("core.view_review_questions_for_track", predicates.is_event_owner)
rules.add_perm("core.view_tracks_for_event", rules.is_authenticated)
rules.add_perm("core.view_activity_registrations_for_event", predicates.is_event_owner)
rules.add_perm(
    "core.view_registrations_for_activity",
    predicates.is_activity_owner | predicates.is_event_owner,
)
rules.add_perm("core.register_self_into_event", rules.is_authenticated)
rules.add_perm("core.register_self_into_activity", predicates.is_registered_to_event)
rules.add_perm("core.add_submission_to_track", predicates.is_registered_to_event)
rules.add_perm("core.change_submission", predicates.is_submission_author)
rules.add_perm("core.delete_submission", predicates.is_submission_author)
