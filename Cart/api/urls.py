from django.urls import path
from .views import *


urlpatterns = [
   path ( 'add_to_cart/',  CartItemCreationView.as_view(), name='add_to_cart'),
   path ("cart_items/<int:store_id>/", CartListView.as_view(), name="cart_items"),
   path ("update_cart_item/<int:pk>/", CartItemUpdateView.as_view(), name="update_cart_item"),
   path ( 'delete_cart_item/<int:pk>/', CartItemDeletionView.as_view(), name='delete_cart_item'),   
]