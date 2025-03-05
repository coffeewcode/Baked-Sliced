from rest_framework import serializers
from .models import Product, Category
from additional.models import Additional
from additional.serializer import AdditionalSerializer
from utils.sales_validations import price_validator, stock_quantity_validator


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_field = ["id"]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    additional = serializers.PrimaryKeyRelatedField(
        queryset=Additional.objects.all(), many=True, required=False
    )

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["id"]

    def validate_additional_available(self, value):
        errors = []

        inactive_additional = [
            additional.id for additional in value if not additional.is_active
        ]
        out_of_stock_additional = [
            additional.id for additional in value if additional.stock_quantity <= 0
        ]

        if inactive_additional:
            errors.append(
                f"The following additional are inactive: {', '.join(map(str, inactive_additional))}"
            )

        if out_of_stock_additional:
            errors.append(
                f"The following additional are out of stock or have no stock: {', '.join(map(str, out_of_stock_additional))}"
            )

        if errors:
            raise serializers.ValidationError(errors)
        return value

    def validate_stock_quantity(self, value):
        return stock_quantity_validator(value)

    def validate_price(self, value):
        return price_validator(value)


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    additional = AdditionalSerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductListSerializerForOrderItem(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "price"]
