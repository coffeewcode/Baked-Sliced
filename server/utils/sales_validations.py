from decimal import Decimal
from rest_framework import serializers


def stock_quantity_validator(value):
    if value < 0 or value > 100:
        raise serializers.ValidationError(
            "It's not possible to create sold out element"
        )
    return value


def price_validator(value):
    value = Decimal(value)
    if value <= 0:
        raise serializers.ValidationError("The price needs to be bigger than 0")
    return value
