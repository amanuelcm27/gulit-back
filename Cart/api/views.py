from rest_framework.response import Response
from rest_framework.generics import *
from ..models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class CartItemCreationView(CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        store = Store.objects.get(id=request.data.get('store_id'))
        cart, created = Cart.objects.get_or_create(
            owner=self.request.user, store=store)
        product = Product.objects.get(id=request.data.get('product_id'))
        existing_item = CartItem.objects.filter(
            cart=cart, product=product).first()
        if existing_item:
            return Response({"message": "Item already exists in cart"}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(cart=cart)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartListView(ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        store = Store.objects.get(id=self.kwargs.get('store_id'))
        cart = Cart.objects.get(owner=self.request.user, store=store)
        total_price = cart.total_price

        return Response({
            "total_price": total_price,
            "items": serializer.data
        })


class CartItemUpdateView(UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]


class CartItemDeletionView(DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
