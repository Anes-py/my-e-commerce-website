from django.db import models
from django.utils.text import gettext_lazy as _
from django.utils import timezone


class Category(models.Model):
    """
    Represents a product category, which may be nested (parent-child structure).

    Attributes:
        parent (Category): Optional parent category to support nested categories.
        name (str): The name of the category.
        slug (str): URL-friendly unique identifier for the category.
        image (ImageField): Image representing the category.
        created_at (datetime): Timestamp when the category was created.
        updated_at (datetime): Timestamp of the last update.
    """

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True,
        verbose_name=_("parent"),
    )
    name = models.CharField(_("name"), max_length=155)
    slug = models.SlugField(
        _("slug"),
        unique=True,
        blank=True,
        allow_unicode=True,
        help_text=_(
            "It is preferable to leave this field blank so that it will be filled in automatically."
        ),
    )
    image = models.ImageField(_("image"), upload_to='categories/')
    created_at = models.DateTimeField(_("created_at"), default=timezone.now)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
