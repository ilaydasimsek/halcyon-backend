# Generated by Django 4.2.4 on 2024-03-24 10:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="article",
            options={"ordering": ["-is_pinned"]},
        ),
        migrations.AddField(
            model_name="article",
            name="is_pinned",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="article",
            name="title",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]