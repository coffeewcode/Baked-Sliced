from rest_framework import serializers
from utils.manipulate_stock import decrement_stock_default, validate_stock_update
from .models import OrderItem, OrderItemAdditional
from product.models import Product
from utils.sales_validations import stock_quantity_validator
from product.serializer import ProductListSerializer, ProductListSerializerForOrderItem
from additional.models import Additional


class OrderItemAdditionalListSerializer(serializers.ModelSerializer):
    additional_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItemAdditional
        fields = "__all__"

    def get_additional_price(self, obj):
        return obj.additional.price


class OrderItemAdditionalSerializerForOrderItem(serializers.ModelSerializer):
    additional_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItemAdditional
        fields = ["id", "quantity", "additional", "additional_price"]

    def get_additional_price(self, obj):
        return obj.additional.price


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


class OrderItemUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItemAdditional
        fields = ["quantity"]

    def update(self, instance, validated_data):
        new_quantity = validated_data.get("quantity", 0)

        validate_stock_update(self, new_quantity, instance, instance.additional)

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
    product = ProductListSerializerForOrderItem()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
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
            "observation",
            "total_price",
            "quantity",
            "order_item_additional",
        ]
        read_only_fields = ["id", "total_price"]

    def create(self, validated_data):
        additional_items = validated_data.pop("order_item_additional", [])
        product = validated_data["product"]

        total_additional_price = 0

        available_product_additional = product.additional_available.all()

        if not available_product_additional and len(additional_items) > 0:
            raise serializers.ValidationError(
                f"Product {product.name} does not have any additional available."
            )

        for item in additional_items:
            additional = Additional.objects.get(id=item["additional_id"])

            if additional not in available_product_additional:
                raise serializers.ValidationError(
                    f"Additional {additional.name} is not available for product {product.name}."
                )

            total_additional_price += additional.price * item["quantity"]

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

    def update(self, instance, validated_data):
        new_quantity = validated_data.get("quantity", instance.quantity)
        product = validated_data.get("product", instance.product)

        validate_stock_update(self, new_quantity, instance, instance.product)
        instance.total_price = new_quantity * product.price
        instance.quantity = new_quantity
        instance.product = product
        instance.save()

        return instance
