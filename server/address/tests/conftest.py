import pytest
from address.models import Address

@pytest.fixture
def address_data():
    """Provides a dictionary with valid data for creating an Address object."""
    return {
        "name": "Home",
        "num": "123",
        "street": "Main Street",
        "postal_code": "12345-678",
        "city": "São Paulo",
        "state": "SP",
        "observations": "Near the park",
        "complement": "Apartment 12A"
    }

@pytest.fixture
def create_address(db, address_data):
    """Creates and returns an Address object using the provided data."""
    return Address.objects.create(**address_data)
