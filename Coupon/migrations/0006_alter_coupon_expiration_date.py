# Generated by Django 5.1.1 on 2024-10-23 19:08

import Coupon.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Coupon', '0005_coupon_unique_coupon_per_store'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='expiration_date',
            field=models.DateField(default=Coupon.models.default_expiration_date),
        ),
    ]