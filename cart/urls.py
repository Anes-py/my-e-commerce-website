from django.urls import path

from . import views

urlpatterns = [
    path('add/<str:product_id>/', views.add_to_cart, name='cart-add'),
    ]
