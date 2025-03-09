from additional.models import Additional
from rest_framework import serializers


class OrderProcessService:
    @staticmethod
    def calculate_total_additional_price(
        additional_items_requested, product_additional_available, product_name
    ):
        total_additional_price = 0
        for item in additional_items_requested:
            additional = Additional.objects.get(id=item["additional_id"])

            if additional not in product_additional_available:
                raise serializers.ValidationError(
                    f"Additional {additional.name} is not available for product {product_name}."
                )
            total_additional_price += additional.price * item["quantity"]
        return total_additional_price
