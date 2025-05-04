import datetime
from unittest.mock import MagicMock, patch
import pytest
from shopping_cart.models import (
    ShoppingCartItem,
    ShoppingCart,
    ShoppingCartItemAdditional,
)
from django.db import models


@patch("order.models.Order.objects.create")
@patch("order.serializer.OrderItemSerializer")
@pytest.mark.django_db
def test_convert_to_order(mock_order_create, shopping_cart):
    mock_queryset = MagicMock()
    mock_delete = MagicMock()
    mock_queryset.delete.return_value = mock_delete

    mock_order = MagicMock()

    mock_order_create.return_value = mock_order
    order = shopping_cart.convert_to_order()
    mock_order_create.assert_called_once()
    assert order == mock_order


@pytest.mark.django_db
def test_create_shopping_cart_item_additional_successful(product):
    cart = ShoppingCart.objects.create()
    shopping_cart_item = ShoppingCartItem.objects.create(
        shopping_cart=cart,
        product=product,
        quantity=1,
        observation="Test observations",
    )
    assert shopping_cart_item.product == product
    assert shopping_cart_item.product.id == product.id
    assert shopping_cart_item.quantity == 1
    assert shopping_cart_item.observation == "Test observations"
    assert shopping_cart_item.shopping_cart == cart
    assert ShoppingCartItem.objects.filter(id=shopping_cart_item.id).exists()


@pytest.mark.django_db
def test_create_shopping_cart_successful():
    created_field = ShoppingCart._meta.get_field("created_at")
    updated_field = ShoppingCart._meta.get_field("updated_at")

    assert isinstance(created_field, models.DateTimeField)
    assert isinstance(updated_field, models.DateTimeField)
    assert created_field.auto_now_add is True
    assert updated_field.auto_now is True

    shopping_cart = ShoppingCart.objects.create()

    assert shopping_cart.created_at is not None
    assert shopping_cart.updated_at is not None
    assert isinstance(shopping_cart.created_at, datetime.datetime)
    assert isinstance(shopping_cart.updated_at, datetime.datetime)

    original_created = shopping_cart.created_at
    original_updated = shopping_cart.updated_at

    shopping_cart.save()
    assert shopping_cart.created_at == original_created
    assert shopping_cart.updated_at != original_updated


@pytest.mark.django_db
def test_create_shopping_cart_item_additional(additional, shopping_cart_item):

    shopping_cart_item_additional = ShoppingCartItemAdditional.objects.create(
        shopping_cart_item=shopping_cart_item, additional=additional, quantity=1
    )

    assert shopping_cart_item_additional.id is not None
    assert ShoppingCartItemAdditional.objects.count() == 1

    assert shopping_cart_item_additional.shopping_cart_item == shopping_cart_item
    assert shopping_cart_item_additional.additional == additional
    assert shopping_cart_item_additional.quantity == 1

    assert (
        shopping_cart_item_additional in shopping_cart_item.selected_additionals.all()
    )
    assert (
        shopping_cart_item_additional in additional.shoppingcartitemadditional_set.all()
    )

    assert shopping_cart_item_additional.quantity >= 1


@pytest.mark.django_db
def test_create_shopping_cart_item_with_valid_data(product, shopping_cart):
    shopping_cart_item = ShoppingCartItem.objects.create(
        shopping_cart=shopping_cart,
        product=product,
        quantity=1,
        observation="Observation test",
    )

    assert shopping_cart_item.id is not None
    assert shopping_cart_item.shopping_cart == shopping_cart
    assert shopping_cart_item.product == product
    assert shopping_cart_item.quantity == 1
    assert shopping_cart_item.observation == "Observation test"

    assert ShoppingCartItem.objects.count() == 1


@pytest.mark.django_db
def test_create_shopping_cart_item_raise_error_when_attributes_are_missing(): ...
