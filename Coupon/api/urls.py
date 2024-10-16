from django.urls import path
from .views import *


urlpatterns = [
    path('create_coupon/', CouponCreationView.as_view(), name='create_coupon'),
    path('coupons/', CouponsListView.as_view(), name='coupons'),
]