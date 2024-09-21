# Generated by Django 5.1.1 on 2024-09-19 21:59

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('logo', models.ImageField(upload_to='store_images', verbose_name='logo of store')),
                ('slogan', models.CharField(max_length=250)),
                ('p_image_1', models.ImageField(upload_to='store_images', verbose_name='store front page image ')),
                ('p_image_2', models.ImageField(upload_to='store_images', verbose_name='store bottom section image ')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('rating', models.DecimalField(decimal_places=1, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('category', models.CharField(choices=[('electronics', 'Electronics'), ('clothing', 'Clothing'), ('home_appliances', 'Home Appliances'), ('books', 'Books'), ('toys', 'Toys'), ('sports', 'Sports'), ('beauty', 'Beauty'), ('automotive', 'Automotive'), ('groceries', 'Groceries'), ('furniture', 'Furniture')], max_length=20)),
                ('description', models.TextField(max_length=850)),
                ('image', models.ImageField(upload_to='store_images')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.store')),
            ],
        ),
    ]
