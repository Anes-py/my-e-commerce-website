from django.shortcuts import render
from django.utils import timezone
from django.db.models import Subquery, OuterRef

from .models import Product, ProductImage

def home_view(request):
    main_image_subquery = ProductImage.objects.filter(
        product=OuterRef('pk'),
        is_main=True,
    ).values('image')[:1]

    discounted_products = Product.objects.with_discount().annotate(main_image=Subquery(main_image_subquery))[:50]

    newest_products = Product.objects.newest().annotate(main_image=Subquery(main_image_subquery))[:50]


    return render(request, 'products/home.html', {
        'discounted_products': discounted_products,
        'newest_products': newest_products,
        })
