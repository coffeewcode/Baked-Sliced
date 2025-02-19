from rest_framework import serializers


def stock_quantity_validator(value: int):
    if value < 0 or value > 100:
        raise serializers.ValidationError("This value is not supported")
    return value


def price_validator(value: float):
    if value <= 0:
        raise serializers.ValidationError("The price needs to be bigger than 0")
    return value
