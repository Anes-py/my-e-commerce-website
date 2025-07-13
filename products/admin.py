from django.contrib import admin

from .models import *

class ProductOptionsInline(admin.TabularInline):
    model = FeatureOption
    extra = 1
    max_num = 20


class SpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1
    max_num = 15


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
    autocomplete_fields = ['category', 'brand']
    search_fields = ['name', 'short_description']

    inlines = [
        SpecificationInline,
        ProductOptionsInline,
        ProductImageInline,

    ]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = [
        'value',
        'is_active',
        'start_date',
        'expire_date',
    ]
    list_editable = ['is_active',]
    list_filter = ['is_active']
    list_display_links = ['value']
    list_per_page = 20
    list_max_show_all = 30
    ordering = ['is_active']
