from django.urls import path
from .views import *


urlpatterns = [
   # path('create_order/', OrderCreationView.as_view(), name='create_order'),
   path('list_orders/', OrderListForUserView.as_view(), name='list_orders'),
   path('list_orders_for_store/', OrderListForStoreView.as_view(), name='list_orders_for_store'),
   path("filter_orders_user/" , OrderFilterForUserView.as_view(), name="filter_orders_user"),
   path("filter_orders_store/" , OrderFilterForStoreView.as_view(), name="filter_orders_user")
   
]