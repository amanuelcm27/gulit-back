from django.urls import path
from .views import *


urlpatterns = [
    path('store_create/', StoreCreationView.as_view(), name='store_create'),
    path ('product_create/', ProductCreationView.as_view(), name='product_create'),
    path ('categories/', CategoryListView.as_view(), name='categories'),
    path ('store_by_user/' , UserCreatedStoreView.as_view(), name='store_by_user'),
    path ('update_store/<int:pk>/', UpdateStoreView.as_view(), name="update_store" ),
    path ("list_products/", UserStoredProductsListView.as_view(), name="list_products"),
    path ("all_stores/", AllStoresView.as_view(), name="all_stores"),
    path ('store/<int:id>/', GetStoreView.as_view(), name='store'),
    path ('store/<int:id>/products/' , GetStoreProductsView.as_view(), name='store_products'),
]