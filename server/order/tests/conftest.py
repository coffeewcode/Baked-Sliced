from decimal import Decimal
from product.models import Category, Product
from additional.models import Additional
from order.models import Order
import pytest

from order.serializer import OrderItemSerializer


@pytest.fixture
def order_item_serializer():
    """Create and return a OrderItemSerializer with order in context."""
    order = Order.objects.create()
    return OrderItemSerializer(context={"order": order})


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
def order_item_data(product, additional):
    """Return a dictionary representing order item data."""
    return {
        "product": product.id,
        "quantity": 2,
        "order_item_additional": [{"additional_id": additional.id, "quantity": 1}],
    }
