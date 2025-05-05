from decimal import Decimal
import pytest

from rest_framework import serializers


@pytest.mark.django_db
def test_create_order_item_without_additional(product, order_item_serializer):
    validated_data = {
        "product": product,
        "quantity": 2,
        "order_item_additional": [],
    }

    order_item = order_item_serializer.create(validated_data=validated_data)

    assert order_item.product == product
    assert order_item.quantity == 2
    assert order_item.total_price == Decimal("20.00")
    assert order_item.order_item_additional.count() == 0


@pytest.mark.django_db
def test_create_order_item_with_valid_additional(
    product, additional, order_item_serializer
):
    product.additional_available.add(additional)

    validated_data = {
        "product": product,
        "quantity": 2,
        "order_item_additional": [{"additional_id": additional.id, "quantity": 1}],
    }

    order_item = order_item_serializer.create(validated_data)

    assert order_item.product == product
    assert order_item.quantity == 2
    assert order_item.total_price == Decimal("25.00")
    assert order_item.order_item_additional.count() == 1
    assert order_item.order_item_additional.first().additional == additional
    assert order_item.order_item_additional.first().quantity == 1


@pytest.mark.django_db
def test_create_order_item_with_invalid_additional(
    product, additional, order_item_serializer
):

    validated_data = {
        "product": product,
        "quantity": 2,
        "order_item_additional": [{"additional_id": additional.id, "quantity": 1}],
    }

    with pytest.raises(serializers.ValidationError) as exc_info:
        order_item_serializer.create(validated_data)

    assert f"Product {product.name} does not have any additional available." in str(
        exc_info.value
    )


@pytest.mark.django_db
def test_create_order_item_with_product_without_additional(
    product, order_item_serializer
):
    validated_data = {
        "product": product,
        "quantity": 2,
        "order_item_additional": [{"additional_id": 1, "quantity": 1}],
    }

    with pytest.raises(serializers.ValidationError) as exc_info:
        order_item_serializer.create(validated_data)

    assert f"Product {product.name} does not have any additional available." in str(
        exc_info.value
    )


@pytest.mark.django_db
def test_total_price_calculation(product, additional, order_item_serializer):
    product.additional_available.add(additional)

    validated_data = {
        "product": product,
        "quantity": 3,
        "order_item_additional": [{"additional_id": additional.id, "quantity": 2}],
    }

    order_item = order_item_serializer.create(validated_data)

    total_product_price = product.price * validated_data["quantity"]
    total_additional_price = additional.price * 2
    expected_total_price = total_product_price + total_additional_price

    assert order_item.total_price == expected_total_price


@pytest.mark.django_db
def test_update_order_item(product, order_item_serializer):
    validated_data = {
        "product": product,
        "quantity": 2,
        "order_item_additional": [{"additional_id": 1, "quantity": 1}],
    }

    with pytest.raises(serializers.ValidationError) as exc_info:
        order_item_serializer.create(validated_data)

    assert f"Product {product.name} does not have any additional available." in str(
        exc_info.value
    )


# update a project and finish at is changed
# test comportament when no values are passsed in create and update
