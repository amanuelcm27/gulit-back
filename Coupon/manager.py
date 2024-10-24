from django.db import models
from django.utils import timezone

class CouponManager(models.Manager):
    def update_expired_coupons(self):
        print('update expirty exectured')
        today = timezone.now()
        print(today)
        self.filter(expired=False, expiration_date__lt=today).update(expired=True)

