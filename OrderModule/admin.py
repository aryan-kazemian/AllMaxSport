from django.contrib import admin
from .models import Order, OrderItem, DiscountCode

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ['product', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_id', 'customer', 'customer_name', 'order_status',
        'total', 'order_date', 'estimated_delivery_date', 'shipped_at'
    )
    list_filter = ('order_status', 'method', 'order_date', 'shipped_at')
    search_fields = ('order_id', 'customer__username', 'customer_name', 'carrier', 'postal_code')
    date_hierarchy = 'order_date'
    ordering = ('-order_date',)
    inlines = [OrderItemInline]

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'percentage', 'expire_date')
    search_fields = ('code',)
    list_filter = ('expire_date',)
    ordering = ('code',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__order_id', 'product__name')
