from rest_framework import serializers
from ..models import *
from Cart.api.serializers import CartSerializer
from Store.api.serializers import StoreSerializer
from Account.api.serializers import UserSerializer
class OrderSerlializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    creator = UserSerializer(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00 , required=False)
    class Meta:
        model = Order
        fields = ('id' , 'order_id' , 'cart' , 'store' , 'creator' , 'status' , 'total_price' , 'date_created')