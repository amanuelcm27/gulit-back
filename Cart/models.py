from django.db import models
from Account.models import User
from Store.models import Store, Product
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
class Cart (models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    checked_out = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.owner.username}'s cart in {self.store.name} checked out : {self.checked_out} "
    
    def update_total(self):
        self.total_price = sum([item.sub_total for item in self.items.all()])
        self.save()
    
    def checkout(self):
        if not self.checked_out:
            self.checked_out = True 
            self.save()
        else:
            raise ValueError("Cart has already been checked out.")
        
    def clean(self):
        #only one non-checked-out cart can exist for a user and store
        if not self.checked_out and Cart.objects.filter(owner=self.owner, store=self.store, checked_out=False).exists():
            raise ValidationError("A non-checked-out cart already exists for this store. (only one non-checked-out cart can exist for a user and store)")
        
        
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE , null=True )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)] , default= 1)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)] , default=0.00)  
    
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
        
    def update_subtotal(self):
        self.sub_total = self.product.price * self.quantity
        self.cart.update_total()
        self.save()