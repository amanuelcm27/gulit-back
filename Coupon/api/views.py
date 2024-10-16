from rest_framework.response import Response
from rest_framework.generics import *
from ..models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


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
        if days:
            coupon.set_expiration(int(days))

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CouponsListView(ListAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        store = Store.objects.get(owner=self.request.user)
        return Coupon.objects.filter(store=store)