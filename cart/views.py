from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from products.models import Product
from .models import Cart, CartItem
from .forms import AddToCartForm

@require_POST
def add_to_cart(request, product_id):
    form = AddToCartForm(request.POST)
    if not form.is_valid():
        return redirect('home')

    product = get_object_or_404(Product, pk=product_id)

    color = form.cleaned_data['color']
    size = form.cleaned_data['size']
    quantity = form.cleaned_data['quantity']

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user,
        )
    else:
        if not request.session.session_key:
            session_key = request.session.create()
        session_key = request.session.session_key

        cart, _ = Cart.objects.get_or_create(
            session_key=session_key,
            user=None,
        )


    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        color=color,
        size=size,
    )
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity
    cart_item.save()

    return redirect('home')
