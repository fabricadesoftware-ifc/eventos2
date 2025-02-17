# Generated by Django 3.0.6 on 2020-10-27 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0026_auto_20201020_1802"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="track",
            options={
                "permissions": [
                    ("add_submission_to_track", "Can add a submission to a track"),
                    (
                        "view_review_questions_for_track",
                        "Can view review questions for a track",
                    ),
                ]
            },
        ),
    ]
