# Generated by Django 4.0 on 2021-12-14 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0027_auto_20201027_1943"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="first name"
            ),
        ),
    ]
