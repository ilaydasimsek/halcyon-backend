# Generated by Django 4.2.4 on 2023-08-26 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("yoga_practices", "0003_alter_yogapractice_options"),
        ("yoga_journeys", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="JourneyActiveYogaChallenge",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("activated_at", models.DateTimeField(auto_now_add=True)),
                ("completed_yoga_practices", models.ManyToManyField(to="yoga_practices.yogapractice")),
                (
                    "yoga_challenge",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="yoga_practices.yogachallenge"),
                ),
                (
                    "yoga_journey",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="yoga_journeys.yogajourney"),
                ),
            ],
            options={
                "ordering": ["-activated_at"],
                "unique_together": {("yoga_challenge", "yoga_journey")},
            },
        ),
        migrations.AddField(
            model_name="yogajourney",
            name="active_yoga_challenges",
            field=models.ManyToManyField(
                blank=True, through="yoga_journeys.JourneyActiveYogaChallenge", to="yoga_practices.yogachallenge"
            ),
        ),
    ]
