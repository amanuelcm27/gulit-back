import requests
import os
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from dotenv import load_dotenv
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from .serializers import PaymentMethodSerializer
from ..models import PaymentMethod
from Store.models import Store
from Cart.models import Cart
from Coupon.models import Coupon
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ..models import Transaction
import uuid

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
            store = Store.objects.get(owner=self.request.user)
        except Store.DoesNotExist:
            return Response("Store not found", status=404)

        url = "https://api.chapa.co/v1/subaccount"
        payload = {
            "business_name": business_name,
            "account_name": account_name,
            "bank_code": bank_code,
            "account_number": account_number,
            "split_value": 0.5,
            "split_type": "percentage"
        }
        headers = {
            'Authorization': f'Bearer {chapa_key}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=payload, headers=headers)
        if (response.status_code == 200):
            payment = PaymentMethod.objects.create(
                owner=self.request.user,
                store=store,
                business_name=business_name,
                account_name=account_name,
                bank_code=bank_code,
                bank_name=bank_name,
                account_number=account_number,
                sub_account_id=response.json().get('data').get('subaccount_id')
            )
            return Response(response.json(), status=200)
        return Response(response.json(), status=400)


class GetPaymentMethod(RetrieveAPIView):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

    def retrieve(self, request, *args, **kwargs):
        store = Store.objects.get(owner=request.user)
        try:
            payment_method = PaymentMethod.objects.get(
                store=store, owner=request.user)
            serializer = self.get_serializer(payment_method)
            return Response(serializer.data, status=200)
        except PaymentMethod.DoesNotExist:
            return Response({"payment_method_set": False}, status=200)


class InitializePayment(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cart_id = request.data.get('cart_id')
        store = Store.objects.get(id=request.data.get('store_id'))
        cart = Cart.objects.get(
            id=cart_id,  owner=self.request.user, store=store, checked_out=False)
        return_url = request.data.get('return_url')
        first_name = request.data.get('fname')
        last_name = request.data.get('lname')
        email = request.data.get('email')
        phone_number = request.data.get('phone')
        if not (return_url and first_name and last_name and email and phone_number):
            return Response({"message": "All fields are required"}, status=400)

        payable_amount = str(cart.discounted_price or cart.total_price)
        sub_account_id = store.payment_method.sub_account_id

        if not sub_account_id:
            return Response({"message": "Payment method not set for the store"}, status=400)

        existing_transaction = Transaction.objects.filter(
            cart=cart).order_by('-created_at').first()

        if existing_transaction and existing_transaction.status in ["pending", "completed"]:
            return Response({'checkout_url': existing_transaction.checkout_url}, status=200)

        # Generate a new tx_ref for a retry if the last attempt failed
        tx_ref = existing_transaction.tx_ref if existing_transaction and existing_transaction.status == "failed" else f"gulit-{cart_id}-{uuid.uuid4().hex[:8]}"

        transaction = Transaction.objects.create(  # initialize transaction
            user=request.user,
            cart=cart,
            store=store,
            tx_ref=tx_ref,
            amount=payable_amount,
            status="pending"
        )

        url = "https://api.chapa.co/v1/transaction/initialize"
        payload = {
            "amount": payable_amount,
            "currency": "ETB",
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "tx_ref": tx_ref,
            "callback_url": "http://localhost:8000/api/verify_payment",
            "return_url": return_url,
            "customization": {
                "title": f"{store.name}",
                "description": "Payment for items in cart",
            },
            "subaccounts": {
                "id": sub_account_id
            }
        }
        headers = {
            'Authorization': f'Bearer {chapa_key}',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        checkout_url = ''
        if response.status_code == 200 and data.get('status') == 'success':
            checkout_url = data['data']['checkout_url']
            transaction.checkout_url = checkout_url
            transaction.save()
        else:
            error_message = data['message']
            return Response({'error_message': error_message}, status=400)

        return Response({'checkout_url': checkout_url}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class VerifyPaymentView(APIView):
    def get(self, request, *args, **kwargs):
        tx_ref = request.query_params.get('trx_ref')
        status = request.query_params.get('status')
        print(request.query_params)
        print(request.data)
        # Check that tx_ref and status are provided
        if not tx_ref or not status:
            return Response({"error": "Invalid callback data"}, status=400)

        # Find the transaction using the tx_ref
        try:
            transaction = Transaction.objects.get(tx_ref=tx_ref)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=404)

        # Verify transaction with Chapa if status is 'success'
        if status == "success":
            chapa_verification_url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
            headers = {'Authorization': f'Bearer {chapa_key}'}
            response = requests.get(chapa_verification_url, headers=headers)

            if response.status_code == 200 and response.json().get('status') == 'success':
                transaction.status = "completed"
                transaction.save()
                return Response({"message": "Payment verified successfully"}, status=200)
            else:
                transaction.status = "failed"
                transaction.save()
                return Response({"error": "Payment verification failed"}, status=400)

        #  if the Chapa status is not 'success' make the transaction status 'failed'
        transaction.status = "failed"
        transaction.save()
        return Response({"error": "Payment not successful"}, status=400)


class TransactionStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tx_ref):
        try:
            transaction = Transaction.objects.get(
                tx_ref=tx_ref, user=request.user)
            return Response({"status": transaction.status}, status=200)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=404)
