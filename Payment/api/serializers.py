from ..models import PaymentMethod
from rest_framework import serializers

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ('bank_code', 'bank_name', 'business_name' , 'account_name', 'account_number', 'owner', 'store')   