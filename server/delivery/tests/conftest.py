import pytest
from delivery.models import Delivery, DeliveryType, DeliveryStatus
from address.models import Address

@pytest.fixture
def address(db):
    """Creates and returns an Address object to be used in Delivery tests."""
    return Address.objects.create(
        name="Office",
        num="456",
        street="Corporate Street",
        postal_code="87654-321",
        city="São Paulo",
        state="SP"
    )

@pytest.fixture
def delivery_data(address):
    """Provides valid data for creating a Delivery object."""
    return {
        "address": address,
        "type": DeliveryType.DELIVERY,
        "price": "25.00",
        "estimated_time": "45 minutes",
        "observations": "Handle with care",
        "status": DeliveryStatus.PENDING
    }

@pytest.fixture
def create_delivery(db, delivery_data):
    """Creates and returns a Delivery object using the provided data."""
    return Delivery.objects.create(**delivery_data)
