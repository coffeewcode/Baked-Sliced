from rest_framework import serializers
from .models import Delivery
from address.models import Address

class DeliverySerializer(serializers.ModelSerializer):
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Delivery
        fields = "__all__"
        read_only_fields = ["id"]

    def validate(self, data):
        delivery_type = data.get("type")
        address = data.get("address")

        if delivery_type == "delivery" and not address:
            raise serializers.ValidationError(
                {"address": "An address is required for delivery type 'delivery'."}
            )

        if delivery_type == "store_pickup" and address:
            raise serializers.ValidationError(
                {"address": "An address should not be provided for delivery type 'store_pickup'."}
            )

        return data
