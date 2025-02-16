from django.db import models
import uuid
from utils.decrement_functions import decrement_stock_default


class Additional(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def decrement_stock(self, quantity):
        decrement_stock_default(self, quantity, self.name)
