from django.shortcuts import render
from django.db.models import Subquery, OuterRef

from categories.models import Category
from .models import Product, ProductImage

def home_view(request):
    main_image_subquery = ProductImage.objects.filter(
        product=OuterRef('pk'),
        is_main=True,
    ).values('image')[:1]

    discounted_products = Product.objects.with_discount().annotate(main_image=Subquery(main_image_subquery))[:50]

    newest_products = Product.objects.newest().annotate(main_image=Subquery(main_image_subquery))[:50]

    top_categories = Category.objects.all()[:6]  # demo ***

    return render(request, 'products/home.html', {
        'discounted_products': discounted_products,
        'newest_products': newest_products,
        'top_categories': top_categories
        })
