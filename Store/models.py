from django.db import models
from Account.models import User
from django.apps import apps
from django.core.validators import MinValueValidator, MaxValueValidator
import os
from django.db.models import F

class Store(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    logo = models.ImageField(
        verbose_name="logo of store", upload_to='store_images')
    p_image_1 = models.ImageField(
        verbose_name="store front page image", upload_to="store_images")
    p_image_2 = models.ImageField(
        verbose_name="store bottom section image", upload_to="store_images")
    slogan = models.CharField(max_length=250)
    description = models.TextField(max_length=1500)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def delete_image_file(self, image_field):
        """Helper method to delete an image file if it exists."""
        if image_field and os.path.isfile(image_field.path):
            os.remove(image_field.path)

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Store.objects.get(pk=self.pk)
            # Delete old files if new ones are uploaded
            if old_instance.logo != self.logo:
                self.delete_image_file(old_instance.logo)
            if old_instance.p_image_1 != self.p_image_1:
                self.delete_image_file(old_instance.p_image_1)
            if old_instance.p_image_2 != self.p_image_2:
                self.delete_image_file(old_instance.p_image_2)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.delete_image_file(self.logo)
        self.delete_image_file(self.p_image_1)
        self.delete_image_file(self.p_image_2)
        super().delete(*args, **kwargs)


class Product(models.Model):
    CATEGORY_CHOICES = (
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('home appliances', 'Home Appliances'),
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
                                 MinValueValidator(0), MaxValueValidator(5)], default=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(max_length=850)
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return f'{self.name} from {self.store.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Checking if the store has more than 3 products
        product_count = Product.objects.filter(store=self.store).count()

        if product_count >= 3 and not self.store.active:
            self.store.active = True
            self.store.save()
            
        CartItem = apps.get_model('Cart', 'CartItem') 
        cart_items = CartItem.objects.filter(product=self , cart__checked_out=False)  # Get all CartItems for this product

        for cart_item in cart_items:
            cart_item.update_subtotal()
            
    def average_rating(self):
        ratings = self.ratings.all() 
        if ratings.exists():
            average_rating = sum(rating.rating for rating in ratings) / ratings.count()
            self.rating = round(average_rating, 1) 
            self.save()
       
            
     
class Rating (models.Model):
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.creator}'s rating for {self.product}"