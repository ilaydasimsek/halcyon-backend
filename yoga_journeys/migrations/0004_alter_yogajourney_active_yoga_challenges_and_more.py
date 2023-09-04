# Generated by Django 4.2.4 on 2023-09-03 18:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("yoga_journeys", "0003_alter_journeyactiveyogachallenge_unique_together_and_more"),
        ("yoga_practices", "0004_journeycompletedyogapractice_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="yogajourney",
            name="active_yoga_challenges",
            field=models.ManyToManyField(
                blank=True, through="yoga_practices.JourneyActiveYogaChallenge", to="yoga_practices.yogachallenge"
            ),
        ),
        migrations.AlterField(
            model_name="yogajourney",
            name="completed_yoga_practices",
            field=models.ManyToManyField(
                blank=True, through="yoga_practices.JourneyCompletedYogaPractice", to="yoga_practices.yogapractice"
            ),
        ),
        migrations.DeleteModel(
            name="JourneyActiveYogaChallenge",
        ),
        migrations.DeleteModel(
            name="JourneyCompletedYogaPractice",
        ),
    ]