from django.db import models
from UserModule.models import User
from ProductModule.models import Product

DELIVERY_METHOD_CHOICES = [
    ('standard', 'Standard'),
    ('express', 'Express'),
]

class DiscountCode(models.Model):
    code = models.CharField(max_length=20)
    percentage = models.DecimalField(max_digits=10, decimal_places=2)
    expire_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending_payment', 'Pending Payment'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order_id = models.CharField(max_length=20, unique=True)
    order_date = models.DateTimeField()
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending_payment')

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    customer_name = models.CharField(max_length=200, null=True, blank=True)

    address = models.TextField(null=True, blank=True)
    postal_code = models.CharField(max_length=100, null=True, blank=True)

    carrier = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estimated_delivery_date = models.DateTimeField()
    method = models.CharField(max_length=10, choices=DELIVERY_METHOD_CHOICES)
    code = models.IntegerField()
    message = models.CharField(max_length=255, null=True, blank=True)
    authority = models.CharField(max_length=100, null=True, blank=True)
    fee_type = models.CharField(max_length=50, null=True, blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    discount_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)

    items = models.ManyToManyField(Product, through='OrderItem', related_name='orders')

    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    item_discount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    coupon_discount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    shipping = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.order_status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('order', 'product')
