from rest_framework.generics import *
from rest_framework.response import Response
from ..models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import OrderSerlializer

class OrderCreationView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerlializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(id=request.data.get('cart_id'),  owner=self.request.user, checked_out=False)
            store = Store.objects.get(id=request.data.get('store_id'))
            # for future payment gateway integration goes here
            order = Order.objects.create(cart=cart, creator=request.user, store=store)
            return Response({'message': 'Order created successfully'}, status=201)
        except:
            
            return Response({"message": "Invalid data"}, status=400)
