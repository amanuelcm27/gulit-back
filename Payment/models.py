from django.db import models
from Account.models import User
from Store.models import Store
from Cart.models import Cart

class PaymentMethod(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    store = models.OneToOneField(
        Store, related_name="payment_method", on_delete=models.CASCADE)
    bank_code = models.IntegerField()
    bank_name = models.CharField(max_length=100)
    business_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100)
    sub_account_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.owner.username}'s Payment Method"


class Transaction(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),              # Transaction initiated but not completed
        ("completed", "Completed"),          # Payment completed successfully
        ("failed", "Failed"),                # Payment failed due to an error
        ("cancelled", "Cancelled"),          # Transaction cancelled by user or system
        ("refunded", "Refunded"),            # Payment refunded to the user
        ("expired", "Expired"),              # Transaction expired due to timeout or no action
    ]

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    tx_ref = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    checkout_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.tx_ref} - {self.status}"
