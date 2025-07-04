from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import gettext_lazy as _


class CustomUser(AbstractUser):
    usable_password = models.BooleanField(default=True)


class SiteSettings(models.Model):
    site_name = models.CharField(_("site name"), max_length=155)
    footer_text = models.CharField(_("footer text"), max_length=155, blank=True)
    footer_contact_phone = models.CharField(_("footer contact phone"), max_length=55, blank=True)
    footer_contact_text = models.CharField(_("footer contact text"), max_length=155, blank=True)
    footer_github_link = models.URLField(_("footer github link"), max_length=100, blank=True)
    footer_telegram_link = models.URLField(_("footer telegram link"), max_length=100, blank=True)
    footer_linkedin_link = models.URLField(_("footer linkedin link"), max_length=100, blank=True)
    footer_instagram_link = models.URLField(_("footer instagram link"), max_length=100, blank=True)

    def __str__(self):
        return self.site_name
