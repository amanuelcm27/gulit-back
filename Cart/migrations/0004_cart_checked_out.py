# Generated by Django 5.1.1 on 2024-10-12 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0003_alter_cartitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='checked_out',
            field=models.BooleanField(default=False),
        ),
    ]
