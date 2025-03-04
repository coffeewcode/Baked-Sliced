from decimal import Decimal
from product.models import Category, Product
from additional.models import Additional
import pytest


@pytest.fixture
def product():
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
    return Additional.objects.create(
        name="Test Additional",
        price=Decimal("5.00"),
        stock_quantity=50,
    )


@pytest.fixture
def order_item_data(product, additional):
    return {
        "product": product.id,
        "quantity": 2,
        "order_item_additional": [{"additional_id": additional.id, "quantity": 1}],
    }
