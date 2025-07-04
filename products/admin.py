from django.contrib import admin

from .models import *

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    min_num = 1
    max_num = 20


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'id',
        'price',
        'stock',
        'status',
        'is_active',
        'created_at',
        'updated_at',
    ]
    ordering = ['stock']
    list_display_links = ['name']
    list_per_page = 20
    list_max_show_all = 30
    list_editable = ['status', 'is_active']
    list_filter = ['status', 'is_active', 'category']
    autocomplete_fields = ['category']
    search_fields = ['name', 'short_description']

    inlines = [
        ProductImageInline
    ]
