from additional.models import Additional
import pytest


@pytest.fixture
def additional(db):
    """Returns valid additional data"""
    return {
        "name": "Test Additional",
        "price": 5,
        "stock_quantity": 20,
        "is_active": True,
    }


@pytest.fixture
def additional_object(db):
    """Returns valid additional object"""
    return Additional.objects.create(
        name="Test Additional", price=5, stock_quantity=20, is_active=True
    )
