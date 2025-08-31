# ecommerce_api/urls.py

from django.contrib import admin
from django.urls import path, include

from products.views import (
    home_view,
    product_grid_view,
    product_detail_view,
    category_list_view,
    category_detail_view,  # Make sure to import the new view
    order_list_view,
    login_view,
    register_view,
)

urlpatterns = [
    # Admin and API URLs
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
    
    # Frontend URL patterns for rendering HTML pages
    path('', home_view, name='home'),
    path('products-grid/', product_grid_view, name='products-grid'),
    path('products/<int:pk>/', product_detail_view, name='product_detail'),
    path('categories/', category_list_view, name='category_list'),
    path('categories/<int:pk>/', category_detail_view, name='category_detail'), # Add this new path
    path('orders/', order_list_view, name='order_list'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
]