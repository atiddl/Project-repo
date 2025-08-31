from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # Added for default datetime

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', default=1)  # Default to category ID 1
    stock_quantity = models.PositiveIntegerField(default=0)  # Default to 0
    image_url = models.URLField(max_length=200, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)  # Renamed from created_at

    def __str__(self):
        return self.name