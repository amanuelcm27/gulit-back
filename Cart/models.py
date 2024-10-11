from django.db import models
from Account.models import User
from Store.models import Store, Product
from django.core.validators import MinValueValidator, MaxValueValidator


class Cart (models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.owner.username}'s cart in {self.store.name} "
    
    def update_total(self):
        self.total_price = sum([item.sub_total for item in self.items.all()])
        self.save()
        
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE , null=True )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)] , default= 1)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)] , default=0.00)  
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.owner.username}'s cart"

    def save(self, *args, **kwargs):
        # Automatically update the subtotal when the quantity or product price changes
        if self.product:
            self.sub_total = self.product.price * self.quantity
        super().save(*args, **kwargs)
        self.cart.update_total()  # Update the total in the cart
        
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.cart.update_total() # Update the total in the cart