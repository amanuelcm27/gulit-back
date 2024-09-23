from django.db import models
from Account.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Store(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    logo = models.ImageField(
        verbose_name="logo of store", upload_to='store_images')
    slogan = models.CharField(max_length=250)
    p_image_1 = models.ImageField(
        verbose_name="store front page image ", upload_to="store_images")
    p_image_2 = models.ImageField(
        verbose_name="store bottom section image ", upload_to="store_images")

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY_CHOICES = (
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('home_appliances', 'Home Appliances'),
        ('books', 'Books'),
        ('toys', 'Toys'),
        ('sports', 'Sports'),
        ('beauty', 'Beauty'),
        ('automotive', 'Automotive'),
        ('groceries', 'Groceries'),
        ('furniture', 'Furniture'),
    )
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[
                                 MinValueValidator(0), MaxValueValidator(5)])
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(max_length=850)
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return self.name
