# Generated by Django 4.2.4 on 2024-05-25 08:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('yoga_journeys', '0004_alter_yogajourney_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yogajourney',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
