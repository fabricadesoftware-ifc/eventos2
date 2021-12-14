# Generated by Django 3.0.7 on 2020-06-23 19:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_change_names"),
    ]

    operations = [
        migrations.CreateModel(
            name="Submission",
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
                ("deleted_on", models.DateTimeField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(
                        help_text="The submission's name in its native language",
                        max_length=255,
                    ),
                ),
                (
                    "title_english",
                    models.CharField(
                        blank=True,
                        help_text="The submission's name in english",
                        max_length=255,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Track",
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
                ("deleted_on", models.DateTimeField(blank=True, null=True)),
                (
                    "slug",
                    models.CharField(
                        help_text="A unique, readable identifier",
                        max_length=255,
                        unique=True,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="The track's name in its native language",
                        max_length=255,
                    ),
                ),
                (
                    "name_english",
                    models.CharField(
                        blank=True,
                        help_text="The track's name in english",
                        max_length=255,
                    ),
                ),
                ("starts_on", models.DateTimeField()),
                ("ends_on", models.DateTimeField()),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="tracks",
                        to="core.Event",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SubmissionAuthorship",
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
                    "submission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="authorships",
                        to="core.Submission",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="submission_authorships",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="submission",
            name="authors",
            field=models.ManyToManyField(
                related_name="submissions_authored",
                through="core.SubmissionAuthorship",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="submission",
            name="track",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="submissions",
                to="core.Track",
            ),
        ),
    ]
