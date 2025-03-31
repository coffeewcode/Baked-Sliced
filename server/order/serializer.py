from decimal import Decimal
from rest_framework import serializers
from utils.manipulate_stock import validate_stock_and_update
from .models import Order, OrderItem, OrderItemAdditional
from product.models import Product
from additional.models import Additional
from .services import OrderProcessService


class OrderItemAdditionalListSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItemAdditional
        fields = "__all__"


class OrderItemAdditionalSerializerForOrderItem(serializers.ModelSerializer):
    class Meta:
        model = OrderItemAdditional
        fields = ["id", "additional", "additional_data", "quantity"]


class OrderItemAdditionalSerializer(serializers.ModelSerializer):
    additional_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = OrderItemAdditional
        fields = ["additional_id", "quantity"]

    def create(self, validated_data):
        additional = Additional.objects.get(id=validated_data["additional_id"])
        additional.decrement_stock(validated_data["quantity"])
        return OrderItemAdditional.objects.create(
            additional=additional, **validated_data
        )


class OrderItemAdditionalUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItemAdditional
        fields = ["quantity", "additional", "additional_data"]
        read_only_fields = ["additional_data"]

    def update(self, instance, validated_data):
        new_quantity = validated_data.get("quantity", 0)
        new_additional = validated_data.get("additional", instance.additional)

        old_total_additional_price = instance.quantity * Decimal(
            instance.additional_data["price"]
        )

        if instance.additional and instance.additional != new_additional:
            instance.additional.increment_stock(instance.quantity)

        if new_additional and instance.additional != new_additional:
            instance.additional = new_additional
            instance.additional.decrement_stock(instance.quantity)
            instance.additional_data = {}

        if not instance.additional and instance.quantity != new_quantity:
            raise serializers.ValidationError(
                "It's not possible to change the quantity of a non registered additional"
            )

        validate_stock_and_update(self, new_quantity, instance, instance.additional)

        order_item = instance.order_item

        new_total_additional_price = new_quantity * new_additional.price

        price_difference_to_increment = (
            new_total_additional_price - old_total_additional_price
        )

        order_item.total_price += price_difference_to_increment

        instance.quantity = new_quantity

        order_item.save()
        instance.save()
        return instance


class OrderItemListSerializer(serializers.ModelSerializer):
    order_item_additional = OrderItemAdditionalSerializerForOrderItem(
        many=True, read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_data",
            "observation",
            "total_price",
            "quantity",
            "created_at",
            "finished_at",
            "is_delivered",
            "order_item_additional",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    order_item_additional = OrderItemAdditionalSerializer(many=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_data",
            "observation",
            "total_price",
            "quantity",
            "order_item_additional",
        ]
        read_only_fields = ["id", "total_price", "product_data"]

    def create(self, validated_data):
        order_id = validated_data.pop("order")
        additional_items = validated_data.pop("order_item_additional", [])
        product = validated_data["product"]

        product_additional_available = product.additional_available.all()

        if not product_additional_available and len(additional_items) > 0:
            raise serializers.ValidationError(
                f"Product {product.name} does not have any additional available."
            )

        total_additional_price = OrderProcessService.calculate_total_additional_price(
            additional_items, product_additional_available, product.name
        )

        total_product_price = product.price * validated_data["quantity"]
        total_price = total_additional_price + total_product_price

        order_item = OrderItem.objects.create(
            total_price=total_price, order=order_id, **validated_data
        )
        product.decrement_stock(validated_data["quantity"])

        for additional_data in additional_items:
            additional = Additional.objects.get(id=additional_data["additional_id"])
            additional.decrement_stock(additional_data["quantity"])
            OrderItemAdditional.objects.create(
                order_item=order_item,
                additional=additional,
                quantity=additional_data["quantity"],
            )

        return order_item


class OrderItemUpdateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), required=False
    )

    class Meta:
        model = OrderItem
        fields = [
            "product",
            "observation",
            "total_price",
            "quantity",
            "is_delivered",
        ]
        read_only_fields = ["total_price"]

    def update(self, instance, validated_data):
        new_product = validated_data.get("product", instance.product)
        new_product_quantity = validated_data.get("quantity", instance.quantity)
        old_total_product_price = (
            Decimal(instance.product_data["price"]) * instance.quantity
        )

        if instance.product and instance.product != new_product:
            instance.product.increment_stock(instance.quantity)

        if not instance.product and instance.quantity != new_product_quantity:
            raise serializers.ValidationError(
                "It's not possible to change the quantity of a non registered product"
            )

        if new_product and instance.product != new_product:
            instance.product = new_product
            instance.product.decrement_stock(instance.quantity)
            instance.product_data = {}

        if new_product and not instance.is_delivered:

            validate_stock_and_update(
                self, new_product_quantity, instance, instance.product
            )

            new_total_product_price = new_product.price * new_product_quantity
            price_difference_to_increment = (
                new_total_product_price - old_total_product_price
            )
            instance.total_price += price_difference_to_increment
            instance.quantity = new_product_quantity

        instance.observation = validated_data.get("observation", instance.observation)
        instance.is_delivered = validated_data.get(
            "is_delivered", instance.is_delivered
        )

        instance.save()

        return instance
