from django.conf import settings

from categories.models import Category
from .models import SiteSettings


def site_settings(request):
    queryset = SiteSettings.objects.first()
    return {
        'site_settings': queryset,
        'main_image_url_prefix': settings.MEDIA_URL,
        'categories': Category.objects.filter(parent__isnull=True),
        'brands' : Category.objects.all(),
    }

