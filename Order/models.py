from django.db import models
from Cart.models import Cart
from Account.models import User
import uuid

class Order(models.Model):
    status_choices = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Automatically generated UUID
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Store the order total at the time of checkout
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.order_id} by {self.creator.username}"

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.cart.total_price
        super().save(*args, **kwargs)