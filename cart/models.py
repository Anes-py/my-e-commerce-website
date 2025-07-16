from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from products.models import Product, Coupon


class Cart(models.Model):
    """Represents a shopping cart for a logged-in user.

    Attributes:
        user (User): The user owning the cart.
        created_at (datetime): When the cart was created.
        updated_at (datetime): When the cart was last updated.
    """
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='cart',
        null=True,
        blank=True,
        verbose_name=_("user"),
    )
    session_key = models.CharField(_("session_key"), max_length=40)
    created_at = models.DateTimeField(_("created at"), default=timezone.now)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    def __str__(self):
        return f"{_("cart of")}{self.user.username if self.user else 'Guest'}  | {self.session_key}"


class CartItem(models.Model):
    """Represents an item in a shopping cart.

    Attributes:
        cart (Cart): The cart this item belongs to.
        product (Product): The product being added.
        quantity (int): Number of items.
        color (str): Selected color option (if applicable).
        size (str): Selected size option (if applicable).
        coupon (Coupon): Applied coupon (if any).
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("items")
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("product"),
    )
    quantity = models.PositiveIntegerField(_("quantity"), default=1)
    color = models.CharField(_("color"), max_length=10, null=True, blank=True)
    size = models.CharField(_("size"), max_length=55, null=True, blank=True)
    # coupon = models.ForeignKey(
    #     Coupon,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     verbose_name=_("coupon")
    # )

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")
