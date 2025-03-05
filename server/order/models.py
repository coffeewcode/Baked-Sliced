from django.db import models
import uuid
from product.models import Product
from additional.models import Additional
from datetime import datetime


class OrderItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    observation = models.CharField(max_length=200, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
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


class OrderItemAdditional(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    order_item = models.ForeignKey(
        OrderItem, related_name="order_item_additional", on_delete=models.CASCADE
    )
    additional = models.ForeignKey(
        Additional, related_name="order_item_additional", on_delete=models.CASCADE
    )
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity}x {self.additional.name}"
