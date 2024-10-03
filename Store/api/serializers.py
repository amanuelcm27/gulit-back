from rest_framework import serializers
from ..models import *


class StoreSerializer (serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'owner', 'name', 'logo', 'slogan',
                  'p_image_1', 'p_image_2', 'description')


class ProductSerializer (serializers.ModelSerializer):
    class Meta:
        models = Product
        fields = ('id', 'store', 'name', 'price', 'discount',
                  'quantity', 'rating', 'category', 'description', 'image')
