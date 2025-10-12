from django.contrib import admin
from .models import Ticket, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('timestamp',)
    fields = ('sender', 'text', 'file_name', 'file_type', 'file_size', 'file_url', 'timestamp')
    show_change_link = True

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'customer', 'status', 'priority', 'related_order_id', 'created_at', 'updated_at', 'resolved_at')
    list_filter = ('status', 'priority', 'created_at', 'resolved_at')
    search_fields = ('subject', 'customer__username', 'related_order_id', 'customer_name')
    readonly_fields = ('created_at', 'updated_at', 'resolved_at')
    inlines = [MessageInline]
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('subject', 'customer', 'customer_name', 'related_order_id', 'status', 'priority')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'resolved_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'sender', 'text_summary', 'timestamp', 'file_name', 'file_type', 'file_size')
    list_filter = ('sender', 'timestamp')
    search_fields = ('text', 'ticket__subject', 'file_name')
    readonly_fields = ('timestamp',)

    def text_summary(self, obj):
        return obj.text[:50] + ('...' if len(obj.text) > 50 else '')
    text_summary.short_description = 'Message'
