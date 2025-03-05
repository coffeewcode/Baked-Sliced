from decimal import Decimal
from unittest.mock import patch
from additional.models import Additional
from additional.serializer import AdditionalSerializer
import pytest


@pytest.mark.django_db
def test_additional_serializer(additional):
    serializer = AdditionalSerializer(data=additional)
    assert serializer.is_valid(), serializer.errors
    validated_data = serializer.validated_data

    assert validated_data["name"] == "Test Additional"
    assert validated_data["price"] == Decimal("5.00")
    assert validated_data["stock_quantity"] == 20
    assert validated_data["is_active"] is True


@patch("utils.manipulate_stock.decrement_stock_default")
def test_decrement_stock_in_product(mock_decrement_stock_default, additional_object):
    additional_old_stock_quantity = additional_object.stock_quantity
    additional_object.decrement_stock(10)

    assert additional_object.stock_quantity == additional_old_stock_quantity - 10


@patch("utils.manipulate_stock.decrement_stock_default")
def test_decrement_stock_when_there_is_not_stock_available(
    mock_decrement_stock_default, additional_object
):
    mock_decrement_stock_default.side_effect = ValueError(
        "There is no more Test Additional. The stock available is 0."
    )

    with pytest.raises(
        ValueError, match="There is no more Test Additional. The stock available is 0."
    ):
        additional_object.decrement_stock(200)


@patch("utils.manipulate_stock.increment_stock_default")
def test_increment_stock_in_product(mock_decrement_stock_default, additional_object):
    additional_old_stock_quantity = additional_object.stock_quantity
    additional_object.increment_stock(10)
    assert additional_object.stock_quantity == additional_old_stock_quantity + 10


@pytest.mark.django_db
def test_product_throw_an_error_when_price_is_less_than_zero(
    additional,
):

    additional["price"] = -20

    serializer = AdditionalSerializer(data=additional)
    assert not serializer.is_valid()
    assert "price" in serializer.errors
    assert serializer.errors["price"][0] == "The price needs to be bigger than 0"
