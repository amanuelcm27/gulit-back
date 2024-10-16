from rest_framework import serializers
from ..models import *
from Account.api.serializers import UserSerializer 
from Store.api.serializers import ProductSerializer , StoreSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(source='product',  queryset=Product.objects.all(), write_only=True)
    sub_total = serializers.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)] , required=False)   
    class Meta:
        model = CartItem
        fields = ('id', "product", 'product_id', 'quantity', 'sub_total')
        
class CartSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, required=False)
    store = StoreSerializer(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)  # Reference CartItems here

    class Meta:
        model = Cart
        fields = ('id', 'owner', 'store', 'total_price', 'checked_out', 'items')
        
        

