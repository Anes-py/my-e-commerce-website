from django.db import models
from django.utils.text import gettext_lazy as _
from django.utils import timezone

from categories.models import Category

class FeatureOption(models.Model):
    """
    Represents a selectable feature for a product, such as color or size.

    Attributes:
        product (Product): The related product.
        feature (str): Type of feature, either 'Color' or 'Size'.
        value (str): The actual value of the feature (e.g., "Red", "XL").
    """
    class Feature(models.TextChoices):
        Color = 'c', _('Color')
        Size = 's', _('Size')

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='feature_options',
    )
    feature = models.CharField(
        _('feature'),
        max_length=1,
        choices=Feature.choices
    )
    value = models.CharField(_("value"), max_length=155)

    def __str__(self):
        return f"{self.feature}: {self.value}"


class ProductSpecification(models.Model):
    """
    Represents a key-value specification for a product.

    Attributes:
        product (Product): The product this specification belongs to.
        key (str): The name of the specification (e.g., "Material").
        value (str): The value of the specification (e.g., "Cotton").
    """
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='specifications'
    )
    key = models.CharField(_("key"), max_length=55)
    value = models.CharField(_("value"), max_length=55)

    def __str__(self):
        return f"{self.key}: {self.value}"


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


class Discount(models.Model):
    """
    Represents a discount that can be applied to a product.

    Attributes:
        value (decimal): Percentage value of the discount.
        is_active (bool): Whether the discount is currently active.
        start_date (datetime): When the discount becomes active.
        expire_date (datetime): When the discount expires.
    """
    value = models.DecimalField(_("value"), max_digits=10, decimal_places=0, max_length=100)
    is_active = models.BooleanField(_("is active"), default=True)
    start_date = models.DateTimeField(_("start date"), null=True, blank=True)
    expire_date = models.DateTimeField(_("expire date"), null=True, blank=True)

    def __str__(self):
        return f"({self.value} %)"

    def is_valid(self):
        """
        Checks if the discount is active and within its valid date range.

        Returns:
            bool: True if valid, otherwise False.
        """

        now = timezone.now()
        return self.is_active and (self.start_date is None or self.start_date <= now) and (self.expire_date is None or self.expire_date >= now)

    def apply_discount(self, price):
        """
        Applies the discount to a given price.

        Args:
            price (float): The original price.

        Returns:
            float: Price after applying the discount.
        """
        if not self.is_valid():
            return price
        return max(price * (1 - self.value / 100), 0)

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discount")
