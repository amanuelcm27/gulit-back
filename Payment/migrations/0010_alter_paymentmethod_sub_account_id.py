# Generated by Django 5.1.1 on 2024-11-06 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payment', '0009_transaction_coupon_used'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='sub_account_id',
            field=models.CharField(max_length=500),
        ),
    ]
