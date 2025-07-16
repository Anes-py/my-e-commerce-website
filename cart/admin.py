from django.contrib import admin

from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = CartItem
    fields = [
        'product',
        'quantity',
        'color',
        'size',
    ]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'session_key',
        'created_at',
        'updated_at',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    list_display_links = [
        'user',
        'session_key',
    ]
    inlines = [
        CartItemInline,
    ]
    list_per_page = 20
    list_max_show_all = 30
