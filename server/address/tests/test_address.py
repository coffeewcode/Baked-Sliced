import pytest
from address.models import Address
from address.serializers import AddressSerializer

@pytest.mark.django_db
def test_address_creation(create_address, address_data):
    """Tests if an Address object is created successfully."""
    address = create_address
    
    assert Address.objects.count() == 1
    assert address.name == address_data["name"]
    assert address.num == address_data["num"]
    assert address.street == address_data["street"]
    assert address.postal_code == address_data["postal_code"]
    assert address.city == address_data["city"]
    assert address.state == address_data["state"]
    assert address.observations == address_data["observations"]
    assert address.complement == address_data["complement"]


@pytest.mark.django_db
def test_address_serializer_validation(address_data):
    """Tests if the AddressSerializer validates correct data."""
    serializer = AddressSerializer(data=address_data)
    assert serializer.is_valid(), serializer.errors
    validated_data = serializer.validated_data
    
    assert validated_data["name"] == "Home"
    assert validated_data["num"] == "123"
    assert validated_data["street"] == "Main Street"
    assert validated_data["postal_code"] == "12345-678"
    assert validated_data["city"] == "São Paulo"
    assert validated_data["state"] == "SP"
    assert validated_data["observations"] == "Near the park"
    assert validated_data["complement"] == "Apartment 12A"

@pytest.mark.django_db
def test_address_serializer_invalid_postal_code(address_data):
    """Tests if the AddressSerializer rejects an invalid postal code."""
    address_data["postal_code"] = "invalid"
    serializer = AddressSerializer(data=address_data)
    assert not serializer.is_valid()
    assert "postal_code" in serializer.errors
