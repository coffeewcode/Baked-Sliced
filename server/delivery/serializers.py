from rest_framework import serializers
from .models import Delivery
from address.serializers import AddressSerializer

class DeliverySerializer(serializers.ModelSerializer):
    address = AddressSerializer()  

    class Meta:
        model = Delivery
        fields = "__all__" 
        read_only_fields = ["id"]
