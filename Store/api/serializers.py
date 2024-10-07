from rest_framework import serializers
from ..models import *
from Account.api.serializers import UserSerializer 


class StoreSerializer (serializers.ModelSerializer):
    owner  = UserSerializer(read_only=True , required=False )
    class Meta:
        model = Store
        fields = ('id', 'owner', 'name', 'logo', 'slogan',
                  'p_image_1', 'p_image_2', 'description' , 'active')


class ProductSerializer (serializers.ModelSerializer):
    store = StoreSerializer(read_only=True , required=False)
    rating = serializers.DecimalField(max_digits=3, decimal_places=1, validators=[
                                     MinValueValidator(0), MaxValueValidator(5)] , required=False)  
    class Meta:
        model = Product
        fields = ('id', 'store', 'name', 'price', 'discount',
                  'quantity', 'rating', 'category', 'description', 'image')
