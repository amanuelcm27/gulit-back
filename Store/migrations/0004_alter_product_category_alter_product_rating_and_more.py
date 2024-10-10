# Generated by Django 5.1.1 on 2024-10-10 14:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0003_store_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('electronics', 'Electronics'), ('clothing', 'Clothing'), ('home appliances', 'Home Appliances'), ('books', 'Books'), ('toys', 'Toys'), ('sports', 'Sports'), ('beauty', 'Beauty'), ('automotive', 'Automotive'), ('groceries', 'Groceries'), ('furniture', 'Furniture')], max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='store',
            name='description',
            field=models.TextField(max_length=1500),
        ),
        migrations.AlterField(
            model_name='store',
            name='p_image_1',
            field=models.ImageField(upload_to='store_images', verbose_name='store front page image'),
        ),
        migrations.AlterField(
            model_name='store',
            name='p_image_2',
            field=models.ImageField(upload_to='store_images', verbose_name='store bottom section image'),
        ),
    ]