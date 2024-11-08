# Generated by Django 5.1.1 on 2024-11-08 14:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0002_customerprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
