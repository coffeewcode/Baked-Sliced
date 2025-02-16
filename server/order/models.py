from django.db import models
import uuid
from product.models import Product
from additional.models import Additional


class OrderItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="final_product"
    )
    additional = models.ManyToManyField(
        Additional,
        through="OrderItemAdditional",
        related_name="order_items",
        blank=True,
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        total_additional_price = sum(
            additional_item.price for additional_item in self.additional.all()
        )
        self.total_price = (self.product.price + total_additional_price) * self.quantity
        super().save(*args, **kwargs)

    def decrement_stock_request_by_order(self):
        self.product.decrement_stock(self.quantity)

        for additional_item in self.additional.all():
            order_additional_found = OrderItemAdditional.objects.get(
                order_item=self, additional=additional_item
            )
            additional_item.decrement_stock(order_additional_found.quantity)


class OrderItemAdditional(models.Model):
    order_item = models.ForeignKey(
        OrderItem, related_name="order_item_additional", on_delete=models.CASCADE
    )
    additional = models.ForeignKey(
        Additional, related_name="order_item_additional", on_delete=models.CASCADE
    )
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity}x {self.additional.name}"
