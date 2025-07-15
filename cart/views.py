from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from products.models import Product
from .models import Cart, CartItem


@require_POST
def add_to_cart(request, product_id, quantity=1):
    product = get_object_or_404(Product, pk=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user,
        )
    else:
        if not request.session.session_key:
            session_key = request.session.create()
            cart, created = Cart.objects.get_or_create(
                session_key=session_key,
                user=None,
            )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        color=request.POST.get("color"),
        size=request.POST.get("size")
    )
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity
    cart_item.save()


