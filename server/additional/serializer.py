from rest_framework import serializers
from models import Additional


class AdditionalSerializer(serializers.Serializer):
    class Meta:
        model = Additional
        fields = "__all__"
        read_only_fields = ["id"]

    def validate_quantity(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("This value is not supported")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("The price needs to be bigger than 0")
        return value
