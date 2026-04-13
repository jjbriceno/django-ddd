"""Tests for OrderItem entity.

Domain Layer Testing Principles:
- Pure unit tests with no external dependencies
- Test entity creation and validation
"""
from decimal import Decimal

import pytest

from ddd_project.apps.domain.entities import OrderItem
from ddd_project.apps.domain.value_objects import Money, Quantity


class TestOrderItemCreation:
    """Tests for OrderItem creation."""
    
    def test_create_valid_order_item(self, sample_order_item):
        item = sample_order_item()
        assert item.id is not None
        assert item.product_name == "Test Product"
        assert item.unit_price.amount == Decimal("29.99")
        assert item.quantity.value == 2
    
    def test_empty_product_name_raises_error(self, money_usd, quantity):
        with pytest.raises(ValueError) as exc_info:
            OrderItem(
                product_name="",
                unit_price=money_usd(10),
                quantity=quantity(1),
            )
        assert "Product name" in str(exc_info.value)
    
    def test_missing_unit_price_raises_error(self, quantity):
        with pytest.raises(ValueError) as exc_info:
            OrderItem(
                product_name="Test",
                unit_price=None,
                quantity=quantity(1),
            )
        assert "Unit price" in str(exc_info.value)
    
    def test_missing_quantity_raises_error(self, money_usd):
        with pytest.raises(ValueError) as exc_info:
            OrderItem(
                product_name="Test",
                unit_price=money_usd(10),
                quantity=None,
            )
        assert "Quantity" in str(exc_info.value)


class TestOrderItemTotalPrice:
    """Tests for OrderItem total price calculation."""
    
    def test_total_price_calculation(self, sample_order_item):
        item = sample_order_item("Product", 10.00, 3)
        assert item.total_price.amount == 30.00
    
    def test_total_price_with_decimal(self, sample_order_item):
        item = sample_order_item("Product", 9.99, 3)
        assert item.total_price.amount == Decimal("29.97")


class TestOrderItemEquality:
    """Tests for OrderItem equality (by ID)."""
    
    def test_different_id_items_not_equal(self):
        item1 = OrderItem(
            product_name="Product",
            unit_price=Money.create(10, "USD"),
            quantity=Quantity.create(1),
        )
        item2 = OrderItem(
            product_name="Product",
            unit_price=Money.create(10, "USD"),
            quantity=Quantity.create(1),
        )
        assert item1.id != item2.id
