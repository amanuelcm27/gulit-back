from rest_framework import serializers
from ..models import User , CustomerProfile


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username' , 'email' , 'role')
        
        
class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    class Meta:
        model = CustomerProfile
        fields = ('id' ,'user', 'first_name', 'last_name', 'email', 'city', 'state', 'address')