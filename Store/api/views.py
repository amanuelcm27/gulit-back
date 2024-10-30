from rest_framework.generics import *
from rest_framework.response import Response
from ..models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

class StoreCreationView (CreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryListView(APIView):
    def get(self, request):
        categories = Product.CATEGORY_CHOICES
        serialized_categories = [
            category[0] for category in categories]
        return Response(serialized_categories)


class ProductCreationView (CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        store = Store.objects.filter(owner=self.request.user).first()
        serializer.save(store=store)


class UserCreatedStoreView(ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Store.objects.filter(owner=self.request.user)


class UpdateStoreView(UpdateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Store.objects.filter(owner=self.request.user)


class UserStoredProductsListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        store_user_owns = Store.objects.filter(
            owner=self.request.user).first()  # specific store user owns
        return Product.objects.filter(store=store_user_owns)


class AllStoresView(ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def get_queryset(self):
        return Store.objects.filter(active=True)


class GetStoreView(RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    lookup_field = 'id'

    
class FeaturedProductsView(ListAPIView):    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        try:
            store = Store.objects.get(id=self.kwargs['id'])
        except Store.DoesNotExist:
            return Response({"message": "Store not found"}, status=400)
       # fetch only 3 large price products from all products
        return Product.objects.filter(store=store).order_by('-price')[:3]


class StoreProductPagination(PageNumberPagination):
    page_size = 6 
    page_size_query_param = 'page_size'  
    max_page_size = 100  

class GetStoreProductsView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StoreProductPagination
    def get_queryset(self):
        store = Store.objects.get(id=self.kwargs['id'])
        return Product.objects.filter(store=store)


class SearchForStoreView(ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('name')
        return Store.objects.filter(name__icontains=search_query, active=True)


class SearchForProductInAStoreView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StoreProductPagination
    def get_queryset(self):
        search_query = self.request.query_params.get('name')
        store = Store.objects.get(id=self.kwargs['id'])
        return Product.objects.filter( Q(name__icontains=search_query) | Q(category__icontains=search_query), store=store)

class FilterProductsInStore(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StoreProductPagination
    def get_queryset(self):
        price_param = self.request.query_params.get('price')
        rating_param = self.request.query_params.get('rating')
        store = Store.objects.get(id=self.kwargs['id'])
        print(price_param , rating_param)
        return Product.objects.filter(price__lte=price_param, rating__gte=rating_param, store=store)

class MaxMinPriceInAStore(APIView):
    
    def get(self, request, *args, **kwargs):
        store = Store.objects.get(id=kwargs.get('id'))
        products = Product.objects.filter(store=store)
        max_price = products.order_by('-price').first().price
        min_price = products.order_by('price').first().price
        return Response({"max_price": max_price, "min_price": min_price})
    
class GetProductView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_object(self):
        store = get_object_or_404(Store, id=self.kwargs['store_id'])
        product = get_object_or_404(Product, id=self.kwargs['product_id'], store=store)
        return product
    
class ProductUpdateView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    
    
class RateProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        rating_value = request.data.get('rating')
        product_id = request.data.get('product_id')
        store_id = request.data.get("store_id")
        comment = request.data.get('comment')
        
        try:
            product = Product.objects.get(id=product_id, store=store_id)
        except Product.DoesNotExist:
            return Response("No Product Found", status=400)        
        rating, created = Rating.objects.update_or_create(
            creator=user,
            product=product,
            defaults={
                'rating': rating_value,
                'comment': comment
            }
        )
        product.average_rating()
        
        if created:
            message = "Rated Product Successfully"
        else:
            message = "Updated Product Rating Successfully"

        return Response(message, status=200)
           
        
class ProductReviewsView(ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    def get_queryset(self):
        store = Store.objects.get(id=self.kwargs['store_id'])
        product = Product.objects.get(id=self.kwargs['product_id'] , store=store)
        return Rating.objects.filter(product=product).exclude(comment__isnull=True).exclude(comment__exact='').order_by('-created_at')
        
        
    
        
    