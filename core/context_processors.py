from .models import SiteSettings

def site_settings(request):
    """
    Retrieves the site settings along with related banners for the website.

    This function queries the `SiteSettings` model to fetch the site's configuration
    and prefetches related banner fields for performance optimization. It returns the
    first site settings instance and up to 8 slider banners, 2 side banners, and 2 middle banners.

    Returns:
        dict: A dictionary containing:
            - 'site_settings': The first `SiteSettings` instance or None if not found.
            - 'slider_banners': A list of up to 8 slider banners.
            - 'side_banners': A list of up to 2 side banners.
            - 'middle_banners': A list of up to 2 middle banners.
    """
    queryset = SiteSettings.objects.prefetch_related(
        'slider_banners',
        'side_banners',
        'middle_banners',
    ).first()

    if queryset:
        slider_banners = queryset.slider_banners.all()[:8]
        side_banners = queryset.side_banners.all()[:2]
        middle_banners = queryset.middle_banners.all()[:2]
        return {
            'site_settings': queryset,
            'slider_banners': slider_banners,
            'side_banners': side_banners,
            'middle_banners': middle_banners,
        }

    return {
        'site_settings': None,
        'slider_banners': [],
        'side_banners': [],
        'middle_banners': [],
    }
