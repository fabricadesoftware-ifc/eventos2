# Generated by Django 3.0.6 on 2020-09-30 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0021_auto_20200731_1924"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="activity",
            name="slug",
        ),
        migrations.RemoveField(
            model_name="track",
            name="slug",
        ),
    ]
