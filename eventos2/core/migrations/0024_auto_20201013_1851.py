# Generated by Django 3.0.6 on 2020-10-13 18:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0023_trackreviewquestion"),
    ]

    operations = [
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="reviews",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "submission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="reviews",
                        to="core.Submission",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReviewAnswer",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=255)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="answers",
                        to="core.TrackReviewQuestion",
                    ),
                ),
                (
                    "review",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="answers",
                        to="core.Review",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="reviewanswer",
            constraint=models.UniqueConstraint(
                fields=("review", "question"), name="unique_review_answer"
            ),
        ),
        migrations.AddConstraint(
            model_name="review",
            constraint=models.UniqueConstraint(
                fields=("submission", "author"), name="unique_review"
            ),
        ),
    ]
