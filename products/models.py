from django.db import models
from django.utils.text import gettext_lazy as _

from categories.models import Category


class ProductImage(models.Model):
    """
       Stores images related to a product.

       Attributes:
           product (Product): The related product.
           image (ImageField): Image file uploaded.
           is_main (bool): Indicates if the image is the main image for the product.
       """
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(_('is_main'), default=False)

    def __str__(self):
        return self.image.name


class Product(models.Model):
    """
      Represents a product in the store.

      Attributes:
          category (Category): The category the product belongs to.
          name (str): Name of the product.
          slug (str): URL-friendly unique identifier.
          short_description (str): A brief description of the product.
          price (int): Original price of the product.
          stock (int): Available quantity in stock.
          status (str): Availability status of the product.
          is_active (bool): Whether the product is visible/active.
          discount (Discount): Related discount applied to the product.
          created_at (datetime): Timestamp when the product was created.
          updated_at (datetime): Timestamp of last update.
      """
    class ProductStatus(models.TextChoices):
        AVAILABLE = 'a',  _('Available'),
        SOON = 's', _('Coming Soon'),
        NOT_AVAILABLE = 'na', _('Not Available'),

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_("category"),
    )
    name = models.CharField(_("name"), max_length=255)
    slug = models.SlugField(
        _("slug"),
        unique=True,
        blank=True,
        allow_unicode=True,
        help_text=_(
        'It is preferable to leave this field blank so that it will be filled in automatically.'
                   )
    )
    short_description = models.CharField(_("short description"),max_length=155)
    price = models.PositiveIntegerField(_("price"), default=0)
    stock = models.PositiveIntegerField(_("stock"), default=0)
    status = models.CharField(
        _("status"),
        max_length=2,
        choices=ProductStatus.choices
    )
    is_active = models.BooleanField(_("is active"), default=True)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")