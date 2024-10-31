import requests
import os
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from dotenv import load_dotenv
from rest_framework.generics import CreateAPIView , RetrieveAPIView
from .serializers import PaymentMethodSerializer
from ..models import PaymentMethod
from Store.models import Store
load_dotenv()


chapa_key = os.getenv('CHAPA_SECRET_KEY')

class ListBanksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        url = "https://api.chapa.co/v1/banks"
        payload = ''
        headers = {
            'Authorization': f'Bearer {chapa_key}'
        }
        response = requests.get(url, headers=headers, data=payload)
        response = response.json()
        return Response(response, status=200)


class CreatePaymentMethod (APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):
        business_name = self.request.data.get('business_name')
        account_name = self.request.data.get('account_name')
        bank_code = self.request.data.get('bank_code')
        account_number = self.request.data.get('account_number')
        bank_name = self.request.data.get('bank_name')  
        try:
            store =Store.objects.get(owner=self.request.user)
        except Store.DoesNotExist:
            return Response("Store not found", status=404)
        
        url = "https://api.chapa.co/v1/subaccount"
        payload = {
            "business_name": business_name,
            "account_name": account_name,
            "bank_code": bank_code,
            "account_number": account_number,
            "split_value": 0.02,
            "split_type": "percentage"
        }
        headers = {
            'Authorization': f'Bearer {chapa_key}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=payload, headers=headers)
        if (response.status_code == 200):
            payment  = PaymentMethod.objects.create(
                owner=self.request.user,
                store = store,
                business_name=business_name,
                account_name=account_name,
                bank_code=bank_code,
                bank_name = bank_name ,
                account_number=account_number , 
                sub_account_id = response.json().get('data').get('subaccount_id')
            )
            return Response(response.json(), status=200)
        return Response(response.json(), status=400)
    

class GetPaymentMethod(RetrieveAPIView):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    
    def retrieve(self, request, *args, **kwargs):
        store = Store.objects.get(owner=request.user)
        try:
            payment_method = PaymentMethod.objects.get(store=store, owner=request.user)
            serializer = self.get_serializer(payment_method)
            return Response(serializer.data, status=200)
        except PaymentMethod.DoesNotExist:
            return Response({"payment_method_set": False}, status=200)
    