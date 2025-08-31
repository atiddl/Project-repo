from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']  # Basic filtering by category ID
    search_fields = ['name', 'category__name']  # Partial search on name or category name

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]  # Anyone can view/list
        return [IsAuthenticated()]  # Auth required for CRUD

    def get_queryset(self):
        queryset = super().get_queryset()
        # Custom filter for price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Custom filter for stock availability (in_stock=true means stock > 0)
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
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]