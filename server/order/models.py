from django.db import models
import uuid
from product.models import Product
from additional.models import Additional
from datetime import datetime


class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True, default=None)
    is_delivered = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.finished_at and self.is_delivered:
            self.mark_as_finished()
        super().save(*args, **kwargs)

    def mark_as_finished(self):
        if not self.finished_at:
            self.finished_at = datetime.now()


class OrderItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    product_data = models.JSONField(default=dict)
    observation = models.CharField(max_length=200, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.product and not self.product_data:
            self.product_data = self.__populate_product_data(self.product)
        super().save(*args, **kwargs)

    def __populate_product_data(self, product):
        return {
            "name": product.name,
            "description": product.description,
            "price": str(product.price),
            "category": {"name": product.category.name},
        }


class OrderItemAdditional(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    order_item = models.ForeignKey(
        OrderItem, related_name="order_item_additional", on_delete=models.CASCADE
    )
    additional = models.ForeignKey(
        Additional, on_delete=models.SET_NULL, null=True, blank=True
    )
    additional_data = models.JSONField(default=dict)
    quantity = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.additional and not self.additional_data:
            self.additional_data = {
                "name": self.additional.name,
                "description": self.additional.description,
                "price": str(self.additional.price),
            }
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.additional.name}"
