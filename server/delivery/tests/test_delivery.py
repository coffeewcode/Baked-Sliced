import pytest
from delivery.models import Delivery, DeliveryType
from delivery.serializers import DeliverySerializer
from decimal import Decimal

@pytest.mark.django_db
def test_delivery_creation(create_delivery):
    """Tests if a Delivery object is created successfully with the expected values."""
    delivery = create_delivery

    assert Delivery.objects.count() == 1
    assert delivery.type == DeliveryType.DELIVERY
    assert delivery.address.name == "Office"
    assert Decimal(delivery.price) == Decimal("25.00")
    assert delivery.estimated_time == "45 minutes"
    assert delivery.observations == "Handle with care"
    assert delivery.status == "pending"


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
    assert serializer.validated_data["type"] == "delivery"
    assert serializer.validated_data["price"] == Decimal("25.00")
    assert serializer.validated_data["estimated_time"] == "45 minutes"
    assert serializer.validated_data["observations"] == "Handle with care"

@pytest.mark.django_db
def test_delivery_serializer_rejects_invalid_address(delivery_data):
    """Tests if the DeliverySerializer rejects invalid data due to missing or incorrect address."""
    delivery_data["type"] = "store_pickup"
    serializer = DeliverySerializer(data=delivery_data)
    assert not serializer.is_valid()
    assert "address" in serializer.errors

@pytest.mark.django_db
def test_delivery_serializer_requires_address_for_delivery_type(delivery_data):
    """Tests if the DeliverySerializer raises a validation error when 'address' is missing for 'delivery' type."""
    delivery_data["type"] = "delivery"
    delivery_data["address"] = None

    serializer = DeliverySerializer(data=delivery_data)
    assert not serializer.is_valid()

    assert "address" in serializer.errors
    assert serializer.errors["address"] == ["An address is required for delivery type 'delivery'."]

