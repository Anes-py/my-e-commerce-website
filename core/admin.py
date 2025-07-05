from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, SiteSettings, SliderBanners, SideBanners, MiddleBanners
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields':('email',)}),
    )
    fieldsets = UserAdmin.fieldsets


class SliderBannersInline(admin.TabularInline):
    model = SliderBanners
    fields = [
        'image',
        'url',
        'is_active',
        'order',
    ]
    max_num = 8
    extra = 1


class SideBannersInline(admin.TabularInline):
    model = SideBanners
    fields = [
        'image',
        'url',
        'is_active',
        'order',
    ]
    max_num = 2
    min_num = 2


class MiddleBannersInline(admin.TabularInline):
    model = MiddleBanners
    fields = [
        'image',
        'url',
        'is_active',
        'order',
    ]
    max_num = 2
    min_num = 2


@admin.register(SiteSettings)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = [
        'site_name',
    ]
    list_display_links = ['site_name']

    inlines = [
        SliderBannersInline,
        SideBannersInline,
        MiddleBannersInline,
    ]
