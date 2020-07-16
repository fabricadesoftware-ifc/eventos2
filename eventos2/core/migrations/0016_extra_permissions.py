# Generated by Django 3.0.7 on 2020-07-13 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0015_user_public_id"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="event",
            options={
                "permissions": [
                    (
                        "view_registrations_for_event",
                        "Can view registrations for an event",
                    ),
                    ("view_activities_for_event", "Can view activities for an event"),
                    ("view_tracks_for_event", "Can view tracks for an event"),
                    (
                        "view_activity_registrations_for_event",
                        "Can view activity registrations for an event",
                    ),
                    ("register_self_into_event", "Can self-register into an event"),
                ]
            },
        ),
        migrations.AlterModelOptions(
            name="activity",
            options={
                "permissions": [
                    (
                        "register_self_into_activity",
                        "Can self-register into an activity",
                    )
                ]
            },
        ),
        migrations.AlterModelOptions(
            name="track",
            options={
                "permissions": [
                    ("add_submission_to_track", "Can add a submission to a track")
                ]
            },
        ),
    ]
