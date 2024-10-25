from rest_framework.generics import *
from rest_framework.response import Response
from ..models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import *
from django.db.models import Count
from decimal import Decimal
from Coupon.models import Coupon

class OrderCreationView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerlializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(id=request.data.get('cart_id'),  owner=self.request.user, checked_out=False)
            store = Store.objects.get(id=request.data.get('store_id'))
            # for future payment gateway integration goes here
            coupon_used = request.data.get('coupon_used')
            print(coupon_used)
            try:
                coupon = Coupon.objects.get(code=coupon_used)
            except Coupon.DoesNotExist:
                return Response({"message": "Coupon not found"}, status=400)
            
            order = Order.objects.create(
                cart=cart,
                creator=request.user,
                store=store,
                total_price=cart.discounted_price  or cart.total_price  # Use the discounted total here
            )
            coupon.coupon_users.add(request.user)  #  add the user to the coupon users list
            return Response({'message': 'Order created successfully'}, status=201)
        except:
            return Response({"message": "Error in order creation"}, status=400)
        
class OrderListForUserView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerlializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(creator=self.request.user)
    
    
class OrderListForStoreView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerlializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        store = Store.objects.get(owner= self.request.user)
        return Order.objects.filter(creator=self.request.user, store=store)


