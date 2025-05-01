from unittest.mock import patch
import pytest
from shopping_cart.models import ShoppingCartItem
from shopping_cart.views import AddItemsInShoppingCartView


@pytest.mark.django_db
def test_(): ...


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
@patch("shopping_cart.views.get_object_or_404")
def test_create_shopping_cart_raise_404_error_when_no_product_found(): ...


@pytest.mark.django_db
def test_create_shopping_cart_raise_404_error_when_no_additional_found(): ...


@pytest.mark.django_db
def test_create_shopping_cart_raise_404_error_when_no_additional_found(): ...


@pytest.mark.django_db
def test_create_shopping_cart_raise_error_when_attributes_are_missing(): ...


@pytest.mark.django_db
def test_checkout_should_create_order_when_sucessfull(): ...
