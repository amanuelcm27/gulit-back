from django.urls import path
from .views import *


urlpatterns = [
    path('create_coupon/', CouponCreationView.as_view(), name='create_coupon'),
    path('coupons/', CouponsListView.as_view(), name='coupons'),
    path('delete_coupon/<int:pk>/', CouponDeletionView.as_view(), name='delete_coupon'),
    path('apply_coupon/', ApplyCouponView.as_view(), name="apply_coupon")
]