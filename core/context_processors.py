from .models import SiteSettings

def site_settings(request):
    queryset = SiteSettings.objects.first()
    return {
        'site_settings': queryset
    }
