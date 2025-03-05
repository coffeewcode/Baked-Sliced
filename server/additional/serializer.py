from rest_framework import serializers
from .models import Additional
from utils.sales_validations import price_validator, stock_quantity_validator


class AdditionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Additional
        fields = "__all__"
        read_only_fields = ["id"]

    def validate_stock_quantity(self, value):
        return stock_quantity_validator(value)

    def validate_price(self, value):
        return price_validator(value)
