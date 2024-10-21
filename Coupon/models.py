from django.db import models
from Store.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import  timedelta
from django.utils import timezone
from Account.models import User
from Cart.models import Cart
from Store.models import Store

class Coupon (models.Model):
    code = models.CharField(max_length=50 )
    store = models.ForeignKey(Store , on_delete=models.CASCADE)
    coupon_users = models.ManyToManyField(User, related_name='coupons')
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)  # Product-specific coupon
    expiration_date = models.DateField(default=timezone.now().date() + timedelta(days=15))
    expired = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code', 'store'], name='unique_coupon_per_store')  # Unique per store
        ]
    def __str__(self):
        return f'{self.code} from {self.store.name}'
    
    def set_expiration(self, days):
        self.expiration_date = timezone.now().date() + timedelta(days=days)
        self.save()
    def check_expiry(self):
        if timezone.now().date() > self.expiration_date:  # Expiration logic
            if not self.expired:
                self.expired = True
                self.save()
            return True
        return False
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.check_expiry()
    
  

