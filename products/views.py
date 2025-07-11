from django.shortcuts import render
from django.views import generic

from categories.models import Category
from core.models import SiteSettings
from .models import Product, FeatureOption


class HomePageView(generic.TemplateView):
    """Renders the homepage with discounted products, new products, and banners.

    This class-based view renders the site's homepage, providing data such as discounted
    products, newest products, top categories, and promotional banners to the template.

    Attributes:
        template_name (str): The name of the default template (implicitly used in the get method).
    """
    def get(self, request, *args, **kwargs):
        """Fetches and renders homepage data.

        This method retrieves discounted products, newest products, top categories, and
        promotional banners (slider, side, and middle) from the database and passes them
        to the template.

        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: Rendered response with the 'products/home.html' template and required data.
        """
        discounted_products = Product.objects.with_discount()[:50]
        newest_products = Product.objects.newest()[:50]
        top_categories = Category.objects.all()[:6]  # demo ***

        queryset = SiteSettings.objects.prefetch_related(
            'slider_banners',
            'side_banners',
            'middle_banners',
        ).first()

        slider_banners = queryset.slider_banners.all()[:8]
        side_banners = queryset.side_banners.all()[:2]
        middle_banners = queryset.middle_banners.all()[:2]
        return render(self.request, 'products/home.html', {
            'discounted_products': discounted_products,
            'newest_products': newest_products,
            'top_categories': top_categories,
            'slider_banners': slider_banners,
            'side_banners': side_banners,
            'middle_banners': middle_banners,
        })


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
            Product.objects.by_category(category_slug=category_slug)

        brand_slug =

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