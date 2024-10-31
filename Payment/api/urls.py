from django.urls import path
from .views import *


urlpatterns = [
    path('banks/', ListBanksView.as_view() , name='list_banks' ),
    path('create_payment_method/', CreatePaymentMethod.as_view() , name='create_payment_method' ),
    path('get_payment_method/' ,GetPaymentMethod.as_view(), name='get_payment_method') 
   
]