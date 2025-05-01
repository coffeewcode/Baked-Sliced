from decimal import Decimal
import pytest
from additional.models import Additional
from product.models import Category, Product
from shopping_cart.models import ShoppingCart
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
