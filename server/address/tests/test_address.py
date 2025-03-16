import pytest
from address.models import Address
from address.serializers import AddressSerializer

@pytest.mark.django_db
def test_address_creation(create_address):
    """Tests if an Address object is created successfully."""
    address = create_address
    assert Address.objects.count() == 1
    assert address.name == "Home"

@pytest.mark.django_db
def test_address_serializer_validation(address_data):
    """Tests if the AddressSerializer validates correct data."""
    serializer = AddressSerializer(data=address_data)
    assert serializer.is_valid()
    assert serializer.validated_data["name"] == "Home"

@pytest.mark.django_db
def test_address_serializer_invalid_postal_code(address_data):
    """Tests if the AddressSerializer rejects an invalid postal code."""
    address_data["postal_code"] = "invalid"
    serializer = AddressSerializer(data=address_data)
    assert not serializer.is_valid()
    assert "postal_code" in serializer.errors
