from django.db import models
from django.utils import timezone

class CouponManager(models.Manager):
    def update_expired_coupons(self):
        today = timezone.now()
        self.filter(expired=False, expiration_date__lt=today).update(expired=True)

