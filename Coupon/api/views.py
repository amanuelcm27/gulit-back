from rest_framework.response import Response
from rest_framework.generics import *
from ..models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from decimal import Decimal
class CouponCreationView(CreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        store = Store.objects.get(owner=self.request.user)
        days = request.data.get('days')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        coupon = serializer.save(store=store) 
        print(days , type(days))
        if days:
            coupon.set_expiration(int(days))

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CouponsListView(ListAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        store = Store.objects.get(owner=self.request.user)
        Coupon.objects.update_expired_coupons()
        print(Coupon)
        return Coupon.objects.filter(store=store)
    
    
class CouponDeletionView(DestroyAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]


class ApplyCouponView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs): 
        code = request.data.get('coupon_code')
        cart = request.data.get('cart')
        user = self.request.user
        store = Store.objects.get(id=request.data.get('store_id'))

        try:
            coupon = Coupon.objects.get(code=code, store=store)
        except Coupon.DoesNotExist:
            return Response({'message': 'Invalid Coupon Code'}, status=status.HTTP_400_BAD_REQUEST)

        # Checking if the coupon has expired
        if coupon.check_expiry():
            return Response({'message': 'This Coupon has expired'}, status=status.HTTP_400_BAD_REQUEST)

        # Checking if the user has already used this coupon
        if user in coupon.coupon_users.all():
            return Response({'message': 'Coupon already used'}, status=status.HTTP_400_BAD_REQUEST)

        # At this point, the coupon is valid
        original_total_price = cart['total_price']
        updated_cart = cart['items']  # Original cart items
        new_total_price = original_total_price
        discount_applied = False
        
        # Apply coupon to specific product (if defined)
        if coupon.product:
            for item in updated_cart:
                product = item['product']
                sub_total = Decimal(item['sub_total'])

                if product.get('id') == coupon.product.id:
                    discount = coupon.discount
                    new_sub_total = sub_total - (sub_total * (discount / 100))
                    item['sub_total'] = f"{new_sub_total:.2f}"  # Update sub_total after discount
                    discount_applied = True
                    new_total_price = Decimal(new_total_price - sub_total + new_sub_total)

        # Apply coupon to the whole cart (if no specific product is defined)
        else:
            discount = coupon.discount
            new_total_price = original_total_price - (original_total_price * (discount / 100))
            discount_applied = True


        if not discount_applied:
            return Response({'message': 'Coupon not applicable to any products in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Coupon has been successfully applied, save the user
        coupon.coupon_users.add(user)

        # Return the updated cart
        updated_cart = {
            'total_price': f"{new_total_price:.2f}",  
            'id': cart['id'], 
            'items': updated_cart  
        }

        return Response(updated_cart, status=status.HTTP_200_OK)
