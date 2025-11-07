from django.contrib import admin
from .models import Category, Product
from mptt.admin import DraggableMPTTAdmin

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title', 'id')
    list_display_links = ('indented_title',)
    fields = ('name', 'parent') 



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('name',)