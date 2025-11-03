from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
]


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_type = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    material = models.CharField(max_length=255)
    weight_capacity = models.PositiveIntegerField(help_text="Weight capacity in kg", null=True, blank=True)
    display = models.CharField(max_length=100, null=True, blank=True)
    motor_power = models.CharField(max_length=100, null=True, blank=True)
    product_weight = models.PositiveIntegerField(help_text="Weight in kg")
    weight = models.CharField(max_length=100)
    dimensions = models.CharField(max_length=100)
    description = models.TextField()
    warranty = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    sales = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    features = models.JSONField(default=list)
    images = models.JSONField(default=list)

    def __str__(self):
        return self.name
