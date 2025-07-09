from django.shortcuts import render
from django.conf import settings
from django.views import generic
from .models import FeatureOption

from categories.models import Category
from .models import Product


class HomePageView(generic.View):
    def get(self, request, *args, **kwargs):

        discounted_products = Product.objects.with_discount()[:50]

        newest_products = Product.objects.newest()[:50]

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

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        querydict = self.request.GET.copy()

        for key in list(querydict.keys()):
            if querydict.get(key) == '':
                del querydict[key]
        querydict.pop('page', None)
        querystring = querydict.urlencode()

        context['main_image_url_prefix'] = settings.MEDIA_URL
        context['querystring'] = querystring
        return context


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        features_options = FeatureOption.objects.filter(product=self.object)
        context = super().get_context_data(**kwargs)
        context['color_options'] = list(
            features_options
            .filter(feature=FeatureOption.Feature.Color)
            .values_list('value', flat=True)
            .distinct()
        )

        context['size_options'] = list(
            features_options
            .filter(feature=FeatureOption.Feature.Size)
            .values_list('value', flat=True)
            .distinct()
        )
        return context