from django.views import generic
from django.shortcuts import render

from categories.models import Category, Brand
from core.models import SiteSettings
from .models import Product, FeatureOption


class HomeView(generic.TemplateView):
    template_name = 'products/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        site_settings_qs = SiteSettings.objects.first()

        if site_settings_qs:
            context['slider_banners'] = site_settings_qs.slider_banners.all()[:8]
            context['side_banners'] = site_settings_qs.side_banners.all()[:2]
            context['middle_banners'] = site_settings_qs.middle_banners.all()[:2]
        else:
            context['slider_banners'] = []
            context['side_banners'] = []
            context['middle_banners'] = []

        context['discounted_products'] = Product.objects.filter(is_discounted=True)[:12]
        context['newest_products'] = Product.objects.order_by('-created_at')[:12]
        context['top_categories'] = Category.objects.filter(is_top=True)

        return context


class ProductListView(generic.ListView):
    """Displays a list of products with search and filter capabilities.

    This class-based view renders a list of products with options to filter by newest,
    discounted, most expensive, or cheapest, and to search based on a query string.

    Attributes:
        template_name (str): The name of the template for rendering the product list.
        paginate_by (int): Number of products per page (32).
    """
    template_name = 'products/products_list.html'
    paginate_by = 32

    def get_queryset(self):
        """Fetches the product queryset with applied search and filter.

        This method generates a queryset of products based on search (q) and filter (f)
        parameters from the GET request.

        Returns:
            QuerySet: Filtered product queryset.
        """
        queryset = Product.objects.newest()
        search_query = self.request.GET.get('q')
        sort_query = self.request.GET.get('f')

        if search_query:
            queryset = Product.objects.search(search_query)

        sort_map = {
            'newest': Product.objects.newest(),
            'discounted': Product.objects.with_discount(),
            'most_expensive': Product.objects.most_expensive(),
            'cheapest': Product.objects.cheapest(),
        }
        if sort_query in sort_map:
            queryset = sort_map[sort_query]

        category_slug = self.request.GET.get("category_slug")
        if category_slug:
            queryset = Product.objects.by_category(category_slug=category_slug)

        brand_slugs = self.request.GET.getlist("brand_slug")
        if brand_slugs:
            queryset = queryset.filter(brand__slug__in=brand_slugs)  #

        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        if min_price and max_price:
            queryset = Product.objects.active().filter(
                price__gte=min_price, price__lte=max_price,
            )

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Adds additional data to the template context.

        This method adds extra data such as the image URL prefix and filtered query string
        to the context.

        Args:
            object_list (QuerySet, optional): List of objects to render.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context dictionary for the template.
        """
        context = super().get_context_data(**kwargs)
        querydict = self.request.GET.copy()

        for key in list(querydict.keys()):
            if querydict.get(key) == '':
                del querydict[key]
        querydict.pop('page', None)
        querystring = querydict.urlencode()
        context['querystring'] = querystring
        context['categories'] = Category.objects.prefetch_related("children").filter(parent__isnull=True)
        context['brands'] = Brand.objects.all()
        context['selected_brands'] = self.request.GET.getlist('brand_slug')
        return context


class ProductDetailView(generic.DetailView):
    """Displays details of a specific product with its features and specifications.

    This class-based view renders the details of a product, including its color and size
    options, main image, specifications, and final price (with discount applied if valid).
    The product is identified by its slug.

    Attributes:
        model (Model): The Product model for fetching data.
        template_name (str): The name of the template for rendering product details.
        slug_field (str): The slug field in the model.
        slug_url_kwarg (str): The name of the slug parameter in the URL.
    """
    template_name = 'products/product_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        """Optimizes queryset by prefetching related data.

        Returns:
            QuerySet: Product queryset with prefetched feature options, images, and specifications.
        """
        return (Product.objects.active().prefetch_related('feature_options', 'images', 'specifications')
                .select_related('discount', 'category'))

    def get_context_data(self, **kwargs):
        """Adds product details, features, main image, and specifications to the template context.

        This method extracts color and size options, the main product image, specifications,
        and final price (with discount) for the product and adds them to the context.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context dictionary for the template.
        """
        context = super().get_context_data(**kwargs)

        color_qs = (self.object.feature_options
                    .filter(feature=FeatureOption.Feature.Color).distinct())
        color_options = [
            {'code': option.color, 'name': option.get_color_display()}
            for option in color_qs
        ]

        size_options = list(
            self.object.feature_options
            .filter(feature=FeatureOption.Feature.Size)
            .values_list('value', flat=True)
            .distinct()
        )

        context.update({
            'color_options': color_options,
            'size_options': size_options,
        })
        return context
