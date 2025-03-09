from rest_framework import serializers
from utils.manipulate_stock import validate_stock_and_update
from .models import OrderItem, OrderItemAdditional
from product.models import Product
from additional.models import Additional
from .services import OrderProcessService


class OrderItemAdditionalListSerializer(serializers.ModelSerializer):
    additional_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItemAdditional
        fields = "__all__"

    def get_additional_price(self, obj):
        return obj.additional.price


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
        fields = ["quantity"]

    def update(self, instance, validated_data):
        new_quantity = validated_data.get("quantity", 0)

        validate_stock_and_update(self, new_quantity, instance, instance.additional)

        order_item = instance.order_item

        old_total_additional_price = instance.quantity * instance.additional.price
        total_additional_price = sum(
            new_quantity * additional.additional.price
            for additional in order_item.order_item_additional.all()
        )

        order_item.total_price += total_additional_price - old_total_additional_price

        order_item.save()
        instance.quantity = new_quantity
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

        order_item = OrderItem.objects.create(total_price=total_price, **validated_data)
        product.decrement_stock(validated_data["quantity"])

        for additional_data in additional_items:
            additional = Additional.objects.get(id=additional_data["additional_id"])

            OrderItemAdditional.objects.create(
                order_item=order_item,
                additional=additional,
                quantity=additional_data["quantity"],
            )

        return order_item


class OrderItemUpdateSerializer(serializers.ModelSerializer):
    order_item_additional = OrderItemAdditionalSerializer(many=True, required=False)
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
            "order_item_additional",
        ]
        read_only_fields = ["total_price"]

    def update(self, instance, validated_data):
        additional_items = validated_data.pop("order_item_additional", None)
        new_product = validated_data.get("product", instance.product)
        new_product_quantity = validated_data.get("quantity", instance.quantity)

        validate_stock_and_update(
            self, new_product_quantity, instance, instance.product
        )

        if new_product != instance.product:
            instance.product = new_product
            # TODO: when change the instance reference, decrement the old stock_quantity too with the new one
            instance.product_data = {}

        if additional_items is not None:
            product_additional_available = instance.product.additional_available.all()

            if not product_additional_available and additional_items:
                raise serializers.ValidationError(
                    f"Product {instance.product.name} does not have any additional available."
                )

            total_additional_price = (
                OrderProcessService.calculate_total_additional_price(
                    additional_items,
                    product_additional_available,
                    instance.product.name,
                )
            )
            instance.order_item_additional.all().delete()

            for item in additional_items:
                OrderItemAdditional.objects.create(
                    order_item=instance,
                    quantity=item["quantity"],
                )

        instance.total_price = (
            instance.product.price * new_product_quantity + total_additional_price
        )
        instance.observation = validated_data.get("observation", instance.observation)
        instance.quantity = new_product_quantity
        instance.is_delivered = validated_data.get(
            "is_delivered", instance.is_delivered
        )

        instance.save()

        return instance
