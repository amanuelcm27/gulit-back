from rest_framework import serializers
from ..models import Coupon
from Account.api.serializers import UserSerializer
from Store.api.serializers import ProductSerializer, StoreSerializer
class CouponSerializer(serializers.ModelSerializer):
    coupon_users = UserSerializer(read_only=True , many=True)
    store = StoreSerializer(read_only=True , required=False)
    
    class Meta:
        model = Coupon
        fields = ('id', 'code', 'coupon_users', 'discount', 'product',
                  'store', 'expiration_date', 'expired', 'date_created')
