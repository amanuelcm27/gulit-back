from django.urls import path
from .views import *


urlpatterns = [
    path('banks/', ListBanksView.as_view() , name='list_banks' ),
    path('create_payment_method/', CreatePaymentMethod.as_view() , name='create_payment_method' ),
    path('get_payment_method/' ,GetPaymentMethod.as_view(), name='get_payment_method')  ,
    path('initialize_payment/' , InitializePayment.as_view() , name='initialize_payment') , 
    path('verify_payment/' , VerifyPaymentView.as_view() , name='verify_payment') ,
    path('transaction_status/<str:tx_ref>/' , TransactionStatusView.as_view() , name='transaction_status') ,
]