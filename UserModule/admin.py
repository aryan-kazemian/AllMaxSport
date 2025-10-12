from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
            'fields': (
                'first_name', 'last_name', 'email', 'phone', 'profile_image',
                'user_type'
            )
        }),
        ('Address info', {
            'fields': (
                'address_name', 'address_phone', 'province', 'city',
                'address', 'postal_code', 'delivery_notes'
            )
        }),
        ('Purchase info', {
            'fields': (
                'total_orders', 'total_spent', 'average_order_value',
                'first_purchase_date', 'last_purchase_date'
            )
        }),
        ('Important dates', {
            'fields': (
                'last_login', 'password_last_changed',
                'created_at', 'updated_at'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'phone', 'user_type',
                'password1', 'password2'
            ),
        }),
    )
    list_display = (
        'id', 'username', 'email', 'phone', 'user_type',
        'is_staff', 'is_superuser', 'created_at', 'last_login'
    )
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'phone', 'first_name', 'last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'password_last_changed')
