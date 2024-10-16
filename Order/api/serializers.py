from rest_framework import serializers
from ..models import *
from Cart.api.serializers import CartSerializer , CartItemSerializer
from Store.api.serializers import StoreSerializer
from Account.api.serializers import UserSerializer
from Cart.models import CartItem
from Store.models import Product


class OrderSerlializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    creator = UserSerializer(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00 , required=False)
    class Meta:
        model = Order
        fields = ('id' , 'order_id' , 'cart', 'store' , 'creator' , 'status' , 'total_price' , 'date_created')
        
class ProductOrderCountSerializer(serializers.ModelSerializer):
    order_count = serializers.IntegerField(read_only=True)  # This is the annotated field from the queryset

    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'order_count'] 
        
        
class ProductOrderDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()  # Custom field for the user who ordered

    class Meta:
        model = CartItem
        fields = ['id', 'user', 'quantity', 'sub_total']

    def get_user(self, obj):
        return UserSerializer(obj.cart.order_by_cart.creator).data