import pytest
from additional.models import Additional
from product.models import Category, Product


@pytest.fixture
def category(db):
    """Creates and returns a Category object."""
    return Category.objects.create(name="Mocked Category")


@pytest.fixture
def product_with_valid_data(category):
    """Returns valid product data with a linked category."""
    return {
        "name": "Chocolate Pizza",
        "description": "For a firewood",
        "category": str(category.id),
        "price": "55.00",
        "stock_quantity": 20,
        "is_active": True,
        "additional_available": [],
    }


@pytest.fixture
def additional_with_valid_data(db):
    """Creates and returns a Additional objects."""

    def _create_additional(is_active=True, stock_quantity=5):
        additional_1 = Additional.objects.create(
            name="Extra Cheese",
            price=4,
            is_active=is_active,
            stock_quantity=stock_quantity,
        )
        additional_2 = Additional.objects.create(
            name="Extra Sauce",
            price=4,
            is_active=is_active,
            stock_quantity=stock_quantity,
        )
        return [additional_1, additional_2]

    return _create_additional


@pytest.fixture
def active_additional():
    """Creates and returns a Additional with property is_active equal True to validate it."""
    return Additional.objects.create(
        name="Active Additional", is_active=True, price=5, stock_quantity=10
    )


@pytest.fixture
def inactive_additional():
    """Creates and returns a Additional with property is_active equal False to validate it."""
    return Additional.objects.create(
        name="Inactive Additional", is_active=False, price=5, stock_quantity=10
    )


@pytest.fixture
def out_of_stock_additional():
    """Creates and returns a Additional out of stock to validate it."""
    return Additional.objects.create(
        name="Out of Stock Additional", is_active=True, price=5, stock_quantity=0
    )


@pytest.fixture
def product(category):
    """Creates and returns a Product to validate the incremental and decrement stock."""
    return Product.objects.create(
        name="Test Product",
        description="Test Description",
        price=10.00,
        category=category,
        stock_quantity=100,
    )
