from django.contrib import admin

from .models import Category, Brand

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]
    list_display_links = ['name',]
    list_filter = ['name',]
    search_fields = ['name']
    autocomplete_fields = ['parent']
    list_per_page = 20
    list_max_show_all = 30

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name',]
    list_display_links = ['name',]
    list_filter = ['name',]
    search_fields = ['name']
    list_per_page = 20
    list_max_show_all = 30
