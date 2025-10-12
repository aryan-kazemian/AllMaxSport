from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'price', 'sale_price', 'stock', 'category',
        'brand', 'product_type', 'status', 'sales', 'created_at', 'updated_at'
    )
    list_filter = ('status', 'category', 'brand', 'product_type', 'created_at')
    search_fields = ('name', 'brand', 'product_type', 'category__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
