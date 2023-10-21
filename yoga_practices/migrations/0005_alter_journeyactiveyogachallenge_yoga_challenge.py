# Generated by Django 4.2.4 on 2023-10-21 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("yoga_practices", "0004_journeycompletedyogapractice_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="journeyactiveyogachallenge",
            name="yoga_challenge",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="active_yoga_challenges",
                to="yoga_practices.yogachallenge",
            ),
        ),
    ]
