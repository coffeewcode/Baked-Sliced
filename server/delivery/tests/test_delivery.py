import pytest
from delivery.models import Delivery, DeliveryType
from delivery.serializers import DeliverySerializer

@pytest.mark.django_db
def test_delivery_creation(create_delivery):
    """Tests if a Delivery object is created successfully."""
    delivery = create_delivery
    assert Delivery.objects.count() == 1
    assert delivery.type == DeliveryType.DELIVERY
    assert delivery.address.name == "Office"

@pytest.mark.django_db
def test_delivery_serializer_valid(delivery_data):
    """Tests if the DeliverySerializer validates correct data."""
    serializer = DeliverySerializer(data={
        "type": "delivery",
        "address": delivery_data["address"].id,
        "price": "25.00",
        "estimated_time": "45 minutes",
        "observations": "Handle with care"
    })
    assert serializer.is_valid()

@pytest.mark.django_db
def test_delivery_serializer_invalid(delivery_data):
    """Tests if the DeliverySerializer rejects invalid data."""
    delivery_data["type"] = "store_pickup"
    serializer = DeliverySerializer(data=delivery_data)
    assert not serializer.is_valid()
    assert "address" in serializer.errors
