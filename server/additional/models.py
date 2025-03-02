from django.db import models
import uuid
from utils.decrement_functions import decrement_stock_default, increment_stock_default


class Additional(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def decrement_stock(self, quantity):
        return decrement_stock_default(self, quantity, self.name)

    def increment_stock(self, quantity):
        return increment_stock_default(self, quantity)
