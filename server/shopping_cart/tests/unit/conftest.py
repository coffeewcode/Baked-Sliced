from decimal import Decimal
from unittest.mock import MagicMock, patch
import pytest
from additional.models import Additional
from product.models import Category, Product
from shopping_cart.models import (
    ShoppingCart,
    ShoppingCartItem,
    ShoppingCartItemAdditional,
)
from shopping_cart.serializers import ShoppingCartItemSerializer


@pytest.fixture
def shopping_cart_serializer():
    """Create and return a ShoppingCartItemSerializer with shopping_cart in context."""
    shopping_cart = ShoppingCart.objects.create()
    return ShoppingCartItemSerializer(context={"shopping_cart": shopping_cart})


@pytest.fixture
def shopping_cart():
    """Return ShoppingCart object"""
    return ShoppingCart.objects.create()


@pytest.fixture
def product():
    """Create and return a Product object."""
    category = Category.objects.create(name="Mocked Category")
    return Product.objects.create(
        name="Test Product",
        description="Test Description",
        price=Decimal("10.00"),
        category=category,
        stock_quantity=100,
    )


@pytest.fixture
def additional():
    """Create and return an Additional object."""
    return Additional.objects.create(
        name="Test Additional",
        price=Decimal("5.00"),
        stock_quantity=50,
    )


@pytest.fixture
def shopping_cart_item(shopping_cart, product):
    shopping_cart_item = ShoppingCartItem.objects.create(
        shopping_cart=shopping_cart, product=product, observation="Test observation"
    )
    return shopping_cart_item


@pytest.fixture
def mock_additional_item():
    mock_additional = MagicMock(spec=ShoppingCartItemAdditional)
    mock_additional.additional.id = 10
    mock_additional.quantity = 1
    return mock_additional
