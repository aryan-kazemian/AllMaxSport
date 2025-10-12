from django.contrib import admin
from .models import Category, Blog, Tag, SEOStatus

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)

class SEOStatusInline(admin.StackedInline):
    model = SEOStatus
    can_delete = False
    extra = 0

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'author', 'category', 'status',
        'seo_score', 'created_date', 'modify_date'
    )
    list_filter = ('status', 'category', 'created_date', 'modify_date')
    search_fields = ('title', 'author', 'keywords', 'category__name')
    ordering = ('-created_date',)
    filter_horizontal = ('tags',)
    inlines = [SEOStatusInline]
    readonly_fields = ('created_date', 'modify_date')

@admin.register(SEOStatus)
class SEOStatusAdmin(admin.ModelAdmin):
    list_display = (
        'blog', 'title_length_status', 'content_length_status',
        'keyword_density_status', 'meta_description_status',
        'headings_status', 'images_status', 'internal_links_status'
    )
    list_filter = (
        'title_length_status', 'content_length_status',
        'keyword_density_status', 'meta_description_status',
        'headings_status', 'images_status', 'internal_links_status'
    )
    search_fields = ('blog__title',)
