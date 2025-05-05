from django.db import models
import uuid
from rest_framework import serializers
from additional.models import Additional
from product.models import Product
from order.models import Order
from order.serializer import OrderItemSerializer


class ShoppingCart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shopping Cart {self.id}"

    def convert_to_order(self):
        order = Order.objects.create()

        for cart_item in self.items.all():
            order_item_data = {
                "product": cart_item.product.id,
                "quantity": cart_item.quantity,
                "order_item_additional": [
                    {
                        "additional_id": additional_item.additional.id,
                        "quantity": additional_item.quantity,
                    }
                    for additional_item in cart_item.selected_additionals.all()
                ],
                "observation": cart_item.observation,
            }
            serializer = OrderItemSerializer(
                data=order_item_data, context={"order": order}
            )
            if serializer.is_valid():
                serializer.save()
            else:
                raise serializers.ValidationError(serializer.errors)

        self.items.all().delete()
        return order


class ShoppingCartItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    shopping_cart = models.ForeignKey(
        ShoppingCart, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    additionals = models.ManyToManyField(
        Additional, through="ShoppingCartItemAdditional", blank=True
    )
    observation = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Cart {self.shopping_cart.id}"


class ShoppingCartItemAdditional(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    shopping_cart_item = models.ForeignKey(
        ShoppingCartItem, on_delete=models.CASCADE, related_name="selected_additionals"
    )
    additional = models.ForeignKey(Additional, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity}x {self.additional.name} for {self.shopping_cart_item.product.name}"
