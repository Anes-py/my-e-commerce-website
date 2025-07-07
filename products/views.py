from django.db.models import Subquery, OuterRef
from django.shortcuts import render
from django.conf import settings
from django.views import generic

from categories.models import Category
from .models import Product, ProductImage


class HomePageView(generic.View):
    def get(self, request, *args, **kwargs):
        main_image_subquery = ProductImage.objects.filter(
            product=OuterRef('pk'),
            is_main=True,
        ).values('image')[:1]

        discounted_products = Product.objects.with_discount().annotate(main_image=Subquery(main_image_subquery))[:50]

        newest_products = Product.objects.newest().annotate(main_image=Subquery(main_image_subquery))[:50]

        top_categories = Category.objects.all()[:6]  # demo ***

        return render(self.request, 'products/home.html', {
            'discounted_products': discounted_products,
            'newest_products': newest_products,
            'top_categories': top_categories,
            'main_image_url_prefix': settings.MEDIA_URL,
        })


class ProductListView(generic.ListView):
    template_name = 'products/products_list.html'
    paginate_by = 32
    def get_queryset(self):
        queryset = Product.objects.newest()
        search_query = self.request.GET.get('q')
        filter_query = self.request.GET.get('f')

        if search_query:
            queryset = Product.objects.search(search_query)

        filter_map = {
            'newest':Product.objects.newest(),
            'discounted':Product.objects.with_discount(),
            'most_expensive':Product.objects.most_expensive(),
            'cheapest':Product.objects.cheapest(),
        }
        if filter_query in filter_map:
            queryset = filter_map[filter_query]


        main_image_subquery = ProductImage.objects.filter(
            product=OuterRef('pk'),
            is_main=True,
        ).values('image')[:1]
        return queryset.annotate(main_image=Subquery(main_image_subquery))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_image_url_prefix'] = settings.MEDIA_URL
        return context
