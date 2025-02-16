from rest_framework import serializers
from models import Product, Category, FinalProduct


class ProductSerializer(serializers.Serializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["id"]
