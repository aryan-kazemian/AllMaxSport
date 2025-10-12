from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta

from .models import Order, DiscountCode
from .serializers import OrderSerializer, CreateOrderSerializer, DiscountCodeSerializer

class OrderDiscountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        get_last_months_profit = request.query_params.get('get_last_months_profit')

        if get_last_months_profit:
            if not user.is_staff:
                return Response({"detail": "Only staff can access profit data"}, status=status.HTTP_403_FORBIDDEN)
            try:
                num_months = int(get_last_months_profit)
                from_date = timezone.now() - timedelta(days=num_months * 30)
                orders = Order.objects.filter(created_at__gte=from_date)
                total_profit = orders.aggregate(total_sum=Sum('total'))['total_sum'] or 0
                return Response({'last_months_profit': total_profit}, status=status.HTTP_200_OK)
            except ValueError:
                return Response({'error': 'Invalid number for get_last_months_profit'}, status=status.HTTP_400_BAD_REQUEST)

        discount_code = request.query_params.get('discount_code')
        discount_code_id = request.query_params.get('discount_code_id')
        order_id = request.query_params.get('id')
        user_id = request.query_params.get('user_id')

        if discount_code == 'true':
            if not user.is_staff:
                return Response({"detail": "Staff only"}, status=status.HTTP_403_FORBIDDEN)
            discounts = DiscountCode.objects.all()
            serializer = DiscountCodeSerializer(discounts, many=True)
            return Response(serializer.data)

        if discount_code_id:
            if not user.is_staff:
                return Response({"detail": "Staff only"}, status=status.HTTP_403_FORBIDDEN)
            discount = get_object_or_404(DiscountCode, id=discount_code_id)
            serializer = DiscountCodeSerializer(discount)
            return Response(serializer.data)

        if order_id:
            order = get_object_or_404(Order, id=order_id)
            if not user.is_staff and order.customer != user:
                return Response({"detail": "You can only access your own orders"}, status=status.HTTP_403_FORBIDDEN)
            serializer = OrderSerializer(order)
            return Response(serializer.data)

        orders = Order.objects.all()
        if not user.is_staff:
            orders = orders.filter(customer=user)
        elif user_id:
            orders = orders.filter(customer_id=user_id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        discount_code = request.query_params.get('discount_code')

        if discount_code == 'true':
            if not user.is_staff:
                return Response({"detail": "Staff only"}, status=status.HTTP_403_FORBIDDEN)
            serializer = DiscountCodeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['customer'] = user.id
        data['customer_name'] = user.get_full_name() or user.username
        serializer = CreateOrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        user = request.user
        discount_code_id = request.query_params.get('discount_code_id')
        order_id = request.query_params.get('id')

        if discount_code_id:
            if not user.is_staff:
                return Response({"detail": "Staff only"}, status=status.HTTP_403_FORBIDDEN)
            discount = get_object_or_404(DiscountCode, id=discount_code_id)
            serializer = DiscountCodeSerializer(discount, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if order_id:
            order = get_object_or_404(Order, id=order_id)
            if not user.is_staff and order.customer != user:
                return Response({"detail": "You can only update your own orders"}, status=status.HTTP_403_FORBIDDEN)
            serializer = CreateOrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Missing id or discount_code_id'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        discount_code_id = request.query_params.get('discount_code_id')
        order_id = request.query_params.get('id')

        if discount_code_id:
            if not user.is_staff:
                return Response({"detail": "Staff only"}, status=status.HTTP_403_FORBIDDEN)
            discount = get_object_or_404(DiscountCode, id=discount_code_id)
            discount.delete()
            return Response({'detail': 'Discount code deleted.'}, status=status.HTTP_204_NO_CONTENT)

        if order_id:
            order = get_object_or_404(Order, id=order_id)
            if not user.is_staff and order.customer != user:
                return Response({"detail": "You can only delete your own orders"}, status=status.HTTP_403_FORBIDDEN)
            order.delete()
            return Response({'detail': 'Order deleted.'}, status=status.HTTP_204_NO_CONTENT)

        return Response({'detail': 'Missing id or discount_code_id'}, status=status.HTTP_400_BAD_REQUEST)
