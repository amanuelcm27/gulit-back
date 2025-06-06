from django.urls import path
from .views import *


urlpatterns = [
    path('store_create/', StoreCreationView.as_view(), name='store_create'),
    path('product_create/', ProductCreationView.as_view(), name='product_create'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('store_by_user/', UserCreatedStoreView.as_view(), name='store_by_user'),
    path('update_store/<int:pk>/', UpdateStoreView.as_view(), name="update_store"),
    path("list_products/", UserStoredProductsListView.as_view(), name="list_products"),
    path("all_stores/", AllStoresView.as_view(), name="all_stores"),
    path('store/<int:id>/', GetStoreView.as_view(), name='store'),
    path('store/<int:id>/products/',
         GetStoreProductsView.as_view(), name='store_products'),
    path('store/<int:id>/featured_products/',FeaturedProductsView.as_view(), name='featured_products'),
    path('stores/search/', SearchForStoreView.as_view(), name='search_store'),
    path('products/search/<int:id>/',
         SearchForProductInAStoreView.as_view(), name='search_product'),
    path("minmax_price/<int:id>/",
         MaxMinPriceInAStore.as_view(), name="minmax_price"),
    path('products/filter/<int:id>/',
         FilterProductsInStore.as_view(), name='filter_products'),
    path('product/<int:store_id>/<int:product_id>/',
         GetProductView.as_view(), name='product'),
    path('update_product/<int:pk>/',
         ProductUpdateView.as_view(), name='update_product'),
    path ('rate_product/' , RateProductView.as_view(), name="rate_product"),
    path ('reviews/<int:store_id>/<int:product_id>/' ,ProductReviewsView.as_view(), name="reviews")
]
