from rest_framework import serializers
from ..models import User, CustomerProfile


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = CustomerProfile
        fields = ('id', 'user', 'first_name', 'last_name',
                  'email', 'city', 'state', 'address')


class UserSerializer(serializers.ModelSerializer):
    profile = CustomerProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'profile')

    