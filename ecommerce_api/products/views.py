# products/views.py

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404, render
from .models import Product, Category, Order
from .serializers import ProductSerializer, UserSerializer, CategorySerializer, OrderSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

# Frontend Views (for rendering HTML templates)
def home_view(request):
    """
    Renders the homepage.
    """
    return render(request, 'home.html')

def product_grid_view(request):
    """
    Renders the product grid page.
    """
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'product_grid.html', context)

def product_detail_view(request, pk):
    """
    Renders a single product detail page.
    """
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'product_detail.html', context)
    
def category_list_view(request):
    """
    Renders the category list page.
    """
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'category_list.html', context)
    
def order_list_view(request):
    """
    Renders the order list page for the authenticated user.
    """
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'order_list.html', context)
    
def login_view(request):
    """
    Renders the login page.
    """
    return render(request, 'login.html')

def register_view(request):
    """
    Renders the registration page.
    """
    return render(request, 'register.html')

# API ViewSets for DRF (for RESTful endpoints)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'category__name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        in_stock = self.request.query_params.get('in_stock')
        if in_stock == 'true':
            queryset = queryset.filter(stock_quantity__gt=0)
        elif in_stock == 'false':
            queryset = queryset.filter(stock_quantity=0)
        
        return queryset

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
def category_detail_view(request, pk):
    """
    Renders a single category detail page.
    """
    category = get_object_or_404(Category, pk=pk)
    context = {'category': category}
    return render(request, 'category_detail.html', context)