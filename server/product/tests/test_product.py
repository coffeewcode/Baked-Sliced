from unittest.mock import MagicMock, patch
from django.forms import ValidationError
import pytest
from product.serializer import ProductSerializer
from product.models import Product, Category
from decimal import Decimal
import uuid
from additional.models import Additional


@pytest.mark.django_db
def test_product_serializer_with_valid_data(product_with_valid_data):
    serializer = ProductSerializer(data=product_with_valid_data)

    assert serializer.is_valid(), serializer.errors

    validated_data = serializer.validated_data
    assert validated_data["name"] == "Chocolate Pizza"
    assert validated_data["price"] == Decimal("55.00")
    assert validated_data["stock_quantity"] == 20
    assert validated_data["is_active"] is True
    assert not validated_data["additional_available"]


@pytest.mark.django_db
def test_product_throw_an_error_when_quantity_is_less_than_zero(
    product_with_valid_data,
):

    product_with_valid_data["stock_quantity"] = -20

    serializer = ProductSerializer(data=product_with_valid_data)
    assert not serializer.is_valid()
    assert "stock_quantity" in serializer.errors
    assert (
        serializer.errors["stock_quantity"][0]
        == "It's not possible to create sold out element"
    )


@pytest.mark.django_db
def test_product_throw_an_error_when_price_is_less_than_zero(
    product_with_valid_data,
):

    product_with_valid_data["price"] = -20

    serializer = ProductSerializer(data=product_with_valid_data)
    assert not serializer.is_valid()
    assert "price" in serializer.errors
    assert serializer.errors["price"][0] == "The price needs to be bigger than 0"


def test_validate_additional_available_valid(additional_with_valid_data):
    additional_items = additional_with_valid_data()
    serializer = ProductSerializer()
    validated_data = serializer.validate_additional_available(additional_items)

    assert validated_data == additional_items


@pytest.mark.django_db
def test_validate_additional_available_valid(category, active_additional):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": "10.00",
        "category": category.id,
        "additional_available": [active_additional.id],
    }
    serializer = ProductSerializer(data=product_data)
    assert serializer.is_valid()


@pytest.mark.django_db
def test_validate_additional_available_inactive(category, inactive_additional):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": "10.00",
        "category": category.id,
        "additional_available": [inactive_additional.id],
    }
    serializer = ProductSerializer(data=product_data)
    assert not serializer.is_valid()
    assert "The following additional are inactive" in str(serializer.errors)


@pytest.mark.django_db
def test_validate_additional_available_out_of_stock(category, out_of_stock_additional):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": "10.00",
        "category": category.id,
        "additional_available": [out_of_stock_additional.id],
    }
    serializer = ProductSerializer(data=product_data)
    assert not serializer.is_valid()
    assert "The following additional are out of stock or have no stock" in str(
        serializer.errors
    )


@pytest.mark.django_db
def test_validate_additional_available_mixed_invalid(
    category, inactive_additional, out_of_stock_additional
):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": "10.00",
        "category": category.id,
        "additional_available": [inactive_additional.id, out_of_stock_additional.id],
    }
    serializer = ProductSerializer(data=product_data)
    assert not serializer.is_valid()
    assert "The following additional are inactive" in str(serializer.errors)
    assert "The following additional are out of stock or have no stock" in str(
        serializer.errors
    )


@patch("utils.manipulate_stock.decrement_stock_default")
def test_decrement_stock_in_product(mock_decrement_stock_default, product):
    product_old_stock_quantity = product.stock_quantity
    product.decrement_stock(10)

    assert product.stock_quantity == product_old_stock_quantity - 10


@patch("utils.manipulate_stock.decrement_stock_default")
def test_decrement_stock_when_there_is_not_stock_available(
    mock_decrement_stock_default, product
):
    mock_decrement_stock_default.side_effect = ValueError(
        "There is no more Test Product. The stock available is 0."
    )

    with pytest.raises(
        ValueError, match="There is no more Test Product. The stock available is 0."
    ):
        product.decrement_stock(200)


@patch("utils.manipulate_stock.increment_stock_default")
def test_increment_stock_in_product(mock_decrement_stock_default, product):
    product_old_stock_quantity = product.stock_quantity
    product.increment_stock(10)
    assert product.stock_quantity == product_old_stock_quantity + 10
