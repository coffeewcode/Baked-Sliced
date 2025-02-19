from rest_framework import serializers
from models import Product, Category, FinalProduct
from utils.sales_validations import price_validator, stock_quantity_validator


class ProductSerializer(serializers.Serializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["id"]

    def validate_quantity(self, value):
        return stock_quantity_validator(value)

    def validate_price(self, value):
        return price_validator(value)
