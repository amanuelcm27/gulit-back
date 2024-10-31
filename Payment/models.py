from django.db import models
from Account.models import User
from Store.models import Store


class PaymentMethod(models.Model):
    owner = models.OneToOneField(User,on_delete=models.CASCADE)
    store = models.OneToOneField(Store,on_delete=models.CASCADE)
    bank_code = models.IntegerField()
    bank_name = models.CharField(max_length=100)
    business_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100)
    sub_account_id = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.owner.username}'s Payment Method"