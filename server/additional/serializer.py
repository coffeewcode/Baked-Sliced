from rest_framework import serializers
from models import Additional
from utils.sales_validations import price_validator, stock_quantity_validator


class AdditionalSerializer(serializers.Serializer):
    class Meta:
        model = Additional
        fields = "__all__"
        read_only_fields = ["id"]

    def validate_quantity(self, value):
        stock_quantity_validator(value)

    def validate_price(self, value):
        price_validator(value)
