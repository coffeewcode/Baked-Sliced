from django.db import models
from additional.models import Additional
import uuid

from utils.decrement_functions import decrement_stock_default


class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=300)
    observation = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    stock_quantity = models.IntegerField(default=0)
    additional_available = models.ManyToManyField(Additional, related_name="products")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def decrement_stock(self, quantity):
        decrement_stock_default(self, quantity, self.name)
