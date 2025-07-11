from django.db import models
from django.db.models import Q
from django.utils.text import gettext_lazy as _
from django.utils import timezone
from django.db.models import Subquery, OuterRef

from categories.models import Category, Brand


class ProductManager(models.Manager):
    """
    Custom manager for Product model, providing commonly used queryset filters.
    """
    def active(self):
        main_image_subquery = ProductImage.objects.filter(
            product=OuterRef('pk'),
            is_main=True,
        ).values('image')[:1]
        """
        Returns only active products.

        Returns:
            QuerySet: Active products.
        """
        return self.get_queryset().filter(is_active=True).annotate(main_image=Subquery(main_image_subquery))

    def newest(self):
        """
        Returns the newest active products, ordered by creation date (descending),
        with related discount data preloaded.

        Returns:
            QuerySet: Newest active products.
        """
        return self.active().order_by('-created_at').select_related('discount')

    def with_discount(self):
        """
        Returns active products with currently valid discounts.

        A discount is considered valid if:
        - It's active.
        - Its start date is in the past or null.
        - Its expire date is in the future or null.

        Returns:
            QuerySet: Products with valid discounts, ordered by stock descending.
        """
        now = timezone.now()
        return self.active().filter(
            Q(discount__start_date__lte=now) | Q(discount__start_date__isnull=True),
            Q(discount__expire_date__gte=now) | Q(discount__expire_date__isnull=True),
            discount__is_active=True,
        ).select_related('discount').order_by('-stock')

    def by_category(self, category_slug):
        """
        Returns active products filtered by category slug.

        Args:
            category_slug (str): The slug of the category.

        Returns:
                QuerySet: Products in the specified category.
        """
        return self.active().filter(category__slug=category_slug).select_related('category')

    def by_brand(self, brand_slug):
        """Filters products by a specific brand using its slug.

        This method retrieves products associated with the given brand slug from the
        active products queryset. It assumes the `active()` method is called first
        to ensure only available products are considered.

        Args:
            brand_slug (str): The slug of the brand to filter by.

        Returns:
            QuerySet: A queryset of active products filtered by the specified brand slug.

        Raises:
            ObjectDoesNotExist: If no brand with the given slug exists (handled by Django's ORM).

        Example:
            >>> Product.objects.by_brand('nike')
            <QuerySet [<Product: Nike Shoe>, <Product: Nike Jacket>]>
        """
        return self.active().filter(brand__slug=brand_slug)

    def search(self, query):
        """
        Searches active products by name or short description (case-insensitive).

        Args:
            query (str): The search keyword.

        Returns:
            QuerySet: Matching active products.
        """
        return self.active().filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query)
        )

    def most_expensive(self):
        """
        Returns active products ordered by price descending.

        Returns:
            QuerySet: Active products sorted from most expensive to cheapest.
        """
        return self.active().order_by('-price')

    def cheapest(self):
        """
        Returns active products ordered by price ascending.

        Returns:
            QuerySet: Active products sorted from cheapest to most expensive.
        """
        return self.active().order_by('price')


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
    class Color(models.TextChoices):
        RED = 'red', _('قرمز')
        BLUE = 'blue', _('آبی')
        GREEN = 'green', _('سبز')
        BLACK = 'black', _('مشکی')
        WHITE = 'white', _('سفید')
        YELLOW = 'yellow', _('زرد')
        ORANGE = 'orange', _('نارنجی')
        PURPLE = 'purple', _('بنفش')
        PINK = 'pink', _('صورتی')
        BROWN = 'brown', _('قهوه‌ای')
        GRAY = 'gray', _('خاکستری')
        SILVER = 'silver', _('نقره‌ای')
        GOLD = 'gold', _('طلایی')
        BEIGE = 'beige', _('بژ')
        MAROON = 'maroon', _('زرشکی')
        NAVY = 'navy', _('سرمه‌ای')
        TEAL = 'teal', _('سبز آبی')
        TURQUOISE = 'turquoise', _('فیروزه‌ای')
        CYAN = 'cyan', _('آبی روشن')
        MAGENTA = 'magenta', _('ارغوانی')
        LIME = 'lime', _('سبز لیمویی')
        OLIVE = 'olive', _('زیتونی')
        INDIGO = 'indigo', _('نیلی')
        VIOLET = 'violet', _('بنفش روشن')
        CORAL = 'coral', _('مرجانی')
        SALMON = 'salmon', _('صورتی سالمونی')
        KHAKI = 'khaki', _('کاکی')
        MINT = 'mint', _('نعنایی')
        PEACH = 'peach', _('هلوئی')
        IVORY = 'ivory', _('عاجی')
        LAVENDER = 'lavender', _('اسطوخودوسی'),

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
    color = models.CharField(
        _('color'), max_length=10,
        choices=Color.choices,
        blank=True,
        help_text=_('If this feature is a color, fill this field and leave the value field empty.')
    )
    value = models.CharField(
        _('value'),
        max_length=55,
        blank=True,
        help_text=_('If this feature is a size, fill this field and leave the color field empty.')
    )

    def __str__(self):
        return f"{self.feature}: {self.value}"

    def get_feature_display(self):
        if self.feature == self.Feature.Color:
            return 'Color'
        return 'Size'


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
        related_name='category-products',
        verbose_name=_("category"),
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='brand-products',
        verbose_name=_("brand")
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
    discount = models.OneToOneField(
        'Discount',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='discount-products',
        verbose_name=_("discount")
    )
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)

    def __str__(self):
        return self.name

    def has_valid_discount(self):
        """
        Checks whether the product has a valid and active discount.

        Returns:
            bool: True if the discount is valid, otherwise False.
        """
        if not self.discount:
            return False

        now = timezone.now()
        return (
                self.discount.is_active and
                (self.discount.start_date is None or self.discount.start_date <= now) and
                (self.discount.expire_date is None or self.discount.expire_date >= now)
        )

    def get_final_price(self):
        """
        Calculates the final price of the product after applying the discount.

        Returns:
            int: Final price after discount, or original price if no valid discount.
        """
        final_price = self.price
        if self.discount and self.discount.is_valid():
            return int(self.discount.apply_discount(final_price))
        return int(final_price)

    objects = ProductManager()

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
    value = models.DecimalField(_("value"), max_digits=10, decimal_places=0)
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


class Coupon(models.Model):
    """
    Represents a coupon that can be applied to a cart.

    Attributes:
        code (str): Unique coupon code.
        discount_type (str): Type of discount (Fixed, Percent, Free Shipping).
        value (decimal): The amount or percent value of the discount.
        is_active (bool): Whether the coupon is currently active.
        start_date (datetime): When the coupon becomes valid.
        expire_date (datetime): When the coupon expires.
    """
    class DiscountType(models.TextChoices):
        FIXED = 'F', _('Fixed Amount')
        PERCENT = 'P', _('Percent')
        FREE_SHIPPING = 'S', _("Free Shipping")

    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    discount_type = models.CharField(max_length=1, choices=[('F', 'Fixed'), ('P', 'Percent'), ('S', 'Free Shipping')])
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    expire_date = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        """
        Checks if the coupon is active and within the valid date range.

        Returns:
            bool: True if valid, otherwise False.
        """
        now = timezone.now()
        return self.is_active and (not self.start_date or self.start_date <= now) and (not self.expire_date or self.expire_date >= now)

    def apply_to_cart(self, total_price, shipping_cost):
        """
        Applies the coupon to the cart's total and/or shipping cost.

        Args:
            total_price (float): The total cart price before discount.
            shipping_cost (float): The current shipping cost.

        Returns:
            tuple: (new_total_price, new_shipping_cost)
        """
        if not self.is_valid():
            return total_price, shipping_cost

        if self.discount_type == 'P':
            total_price = max(total_price * (1 - self.value / 100), 0)

        elif self.discount_type == 'F':
            total_price = max(total_price - self.value, 0)

        elif self.discount_type == 'S':
            shipping_cost = 0

        return total_price, shipping_cost

    class Meta:
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")
