from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework import serializers
from additional.serializer import AdditionalSerializer
from utils.decrement_functions import decrement_stock_default
from .models import OrderItem, OrderItemAdditional
from product.models import Product
from utils.sales_validations import stock_quantity_validator
from product.serializer import ProductListSerializer
from additional.models import Additional


class OrderItemAdditionalSerializer(serializers.ModelSerializer):
    additional = serializers.PrimaryKeyRelatedField(queryset=Additional.objects.all())

    class Meta:
        model = OrderItemAdditional
        fields = ["additional", "quantity"]

    def create(self, validated_data):
        print("validated_data:", validated_data)
        additional = validated_data.get("additional")
        quantity = validated_data.get("quantity", 0)
        print("quantity", quantity)
        print("additional", additional)

        order_item = validated_data.get("order_item")
        print("order", order_item)
        if not order_item:
            raise serializers.ValidationError("Order item is required.")
        order_item_additional = OrderItemAdditional.objects.create(
            order_item=order_item, additional=additional, quantity=quantity
        )

        order_item_additional.save()

        return order_item_additional


class OrderItemListSerializer(serializers.ModelSerializer):
    additional = AdditionalSerializer(many=True)
    product = ProductListSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    additional = OrderItemAdditionalSerializer(many=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "additional",
            "observation",
            "total_price",
            "quantity",
            "created_at",
        ]
        read_only_fields = ["id", "total_price", "created_at"]

    def create(self, validated_data):
        additional_items = validated_data.pop("additional", [])
        print("additional_items", additional_items)
        product = validated_data["product"]
        total_additional_price = sum(
            additional_item["additional"].price * additional_item["quantity"]
            for additional_item in additional_items
        )

        total_product_price = product.price * validated_data["quantity"]

        total_price = total_additional_price + total_product_price

        additional_ids = [
            additional_item["additional"].id for additional_item in additional_items
        ]

        order_item = OrderItem.objects.create(total_price=total_price, **validated_data)
        order_item.additional.set(additional_ids)
        order_item.decrement_stock_default(validated_data["quantity"], product.name)

        for additional_data in additional_items:
            print("additional", additional_data["additional"])
            print("quantity", additional_data["quantity"])
            print("order_item", order_item)

            additional = additional_data["additional"]
            quantity = additional_data["quantity"]
            OrderItemAdditional.objects.create(
                order_item=order_item, additional=additional, quantity=quantity
            )
        order_item.save()
        return order_item

    def update(self, instance, validated_data):
        additional_items = validated_data.pop("additional", None)
        quantity = validated_data.get("quantity", instance.quantity)
        product = validated_data.get("product", instance.product)

        if quantity != instance.quantity:
            if quantity > instance.quantity:
                instance.product.increment(quantity - instance.quantity)
                instance.product.decrement_stock(quantity)
            else:
                instance.product.increment(instance.quantity - quantity)
                instance.product.decrement_stock(quantity)

        return instance
