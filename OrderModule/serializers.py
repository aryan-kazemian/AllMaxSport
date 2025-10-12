from rest_framework import serializers
from .models import Order, OrderItem, DiscountCode
from ProductModule.models import Product

class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ['id', 'code', 'percentage', 'expire_date']

class OrderItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product.id')
    name = serializers.CharField(source='product.name')
    price = serializers.DecimalField(source='product.price', max_digits=12, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ['id', 'name', 'quantity', 'price']

class CreateOrderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='order_items', many=True, read_only=True)
    address = serializers.CharField(allow_blank=True, allow_null=True)
    postal_code = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'order_date', 'customer', 'customer_name', 'carrier', 'order_status',
            'method', 'code', 'estimated_delivery_date', 'items',
            'subtotal', 'shipping', 'tax', 'total',
            'address', 'postal_code'
        ]

class CreateOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='order_items', many=True, read_only=True)
    address = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    postal_code = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = Order
        fields = [
            'order_id', 'order_date', 'order_status', 'customer', 'customer_name',
            'carrier', 'cost', 'estimated_delivery_date', 'method', 'code', 'message',
            'authority', 'fee_type', 'fee', 'subtotal', 'item_discount', 'coupon_discount',
            'shipping', 'tax', 'total', 'address', 'postal_code', 'items'
        ]

    def create(self, validated_data):
        items_data = self.initial_data.get('items', [])
        validated_data.pop('items', None)
        order = Order.objects.create(**validated_data)
        for item in items_data:
            product = Product.objects.get(id=item['id'])
            OrderItem.objects.create(order=order, product=product, quantity=item['quantity'])
        return order

    def update(self, instance, validated_data):
        items_data = self.initial_data.get('items', [])
        validated_data.pop('items', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            instance.order_items.all().delete()
            for item in items_data:
                product = Product.objects.get(id=item['id'])
                OrderItem.objects.create(order=instance, product=product, quantity=item['quantity'])
        return instance
