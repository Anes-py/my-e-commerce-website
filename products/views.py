from django.shortcuts import render
from django.db.models import Subquery, OuterRef, Q
from django.conf import settings
from django.utils import timezone

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
        'top_categories': top_categories,
        'main_image_url_prefix': settings.MEDIA_URL,
        })


def product_list_view(request):
    main_image_subquery = ProductImage.objects.filter(
        product=OuterRef('pk'),
        is_main=True,
    ).values('image')[:1]

    queryset = Product.objects.newest()
    search_query = request.GET.get('q')
    filter_query = request.GET.get('f')

    if search_query:
        queryset = Product.objects.search(search_query)

    if filter_query == 'discounted':
        queryset = Product.objects.with_discount()

    if filter_query == 'most_expensive':
        queryset = Product.objects.most_expensive()

    if filter_query == 'cheapest':
        queryset = Product.objects.cheapest()

    main_image_subquery = ProductImage.objects.filter(
        product=OuterRef('pk'),
        is_main=True,
    ).values('image')[:1]
    queryset = queryset.annotate(main_image=Subquery(main_image_subquery))

    return render(request, 'products/products_list.html', context={
        'product_list': queryset,
        'main_image_url_prefix': settings.MEDIA_URL,
    })