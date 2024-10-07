from rest_framework.generics import *
from rest_framework.response import Response
from ..models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


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
        store_user_owns = Store.objects.filter(owner=self.request.user).first() # specific store user owns
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
    
class GetStoreProductsView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        store = Store.objects.get(id=self.kwargs['id'])
        return Product.objects.filter(store=store)
