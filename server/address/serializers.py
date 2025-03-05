from rest_framework import serializers
from .models import Address
import re

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["id"]

    def validate_postal_code(self, value):
        if not re.match(r'^\d{5}-\d{3}$', value):
            raise serializers.ValidationError("The postal code must follow the format 12345-678.")
        return value
    
    full_address = serializers.SerializerMethodField()

    def get_full_address(self, obj):
        return f"{obj.street}, {obj.city}, {obj.postal_code}"

   