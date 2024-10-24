from rest_framework import serializers
from ..models import Coupon
from Store.models import Product
from Account.api.serializers import UserSerializer
from Store.api.serializers import ProductSerializer, StoreSerializer
class CouponSerializer(serializers.ModelSerializer):
    coupon_users = UserSerializer(read_only=True , many=True)
    store = StoreSerializer(read_only=True , required=False)
    product_id = serializers.PrimaryKeyRelatedField(source='product', queryset=Product.objects.all() , required=False, allow_null=True)
    product = ProductSerializer(read_only=True)
    class Meta:
        model = Coupon
        fields = ('id', 'code', 'coupon_users', 'discount', 'product', 'product_id',
                  'store', 'expiration_date', 'expired', 'date_created')
