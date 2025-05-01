from rest_framework import serializers
from additional.models import Additional
from .models import ShoppingCartItemAdditional, ShoppingCartItem, ShoppingCart


class ShoppingCartItemAdditionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartItemAdditional
        fields = ["id", "additional", "quantity"]


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    additionals = ShoppingCartItemAdditionalSerializer(
        many=True, required=False, source="selected_additionals"
    )

    class Meta:
        model = ShoppingCartItem
        fields = ["product", "quantity", "additionals", "observation"]


class ShoppingCartSerializer(serializers.ModelSerializer):
    items = ShoppingCartItemSerializer(many=True, required=False)

    class Meta:
        model = ShoppingCart
        fields = ["id", "created_at", "updated_at", "items"]
        read_only_fields = ["id", "created_at", "updated_at"]
