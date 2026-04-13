"""Tests for Order aggregate root.

Domain Layer Testing Principles:
- Pure unit tests with no external dependencies
- Test entity creation, business rules, and state transitions
- Test aggregate invariants are maintained
"""
from uuid import uuid4

import pytest

from ddd_project.apps.domain.entities import Order, OrderItem
from ddd_project.apps.domain.value_objects import OrderStatus, Money, Quantity
from ddd_project.apps.domain.exceptions import (
    EmptyOrderError,
    InvalidOrderStatusTransitionError,
    CannotModifyOrderError,
)


class TestOrderCreation:
    """Tests for Order creation."""
    
    def test_create_empty_order(self):
        order = Order()
        assert order.id is not None
        assert order.status == OrderStatus.pending()
        assert order.items == []
        assert order.customer_id is None
        assert order.shipping_address == ""
        assert order.notes == ""
    
    def test_create_order_with_shipping_address(self):
        order = Order(shipping_address="123 Main St")
        assert order.shipping_address == "123 Main St"
    
    def test_create_order_with_customer(self):
        customer_id = uuid4()
        order = Order(customer_id=customer_id)
        assert order.customer_id == customer_id
    
    def test_order_has_timestamps(self):
        order = Order()
        assert order.created_at is not None
        assert order.updated_at is not None


class TestOrderItems:
    """Tests for Order item management."""
    
    def _create_item(self, product_name="Test", unit_price=10.0, qty=1):
        return OrderItem(
            product_name=product_name,
            unit_price=Money.create(unit_price, "USD"),
            quantity=Quantity.create(qty),
        )
    
    def test_add_item_to_pending_order(self):
        order = Order()
        item = self._create_item()
        order.add_item(item)
        assert len(order.items) == 1
        assert order.items[0] == item
    
    def test_add_multiple_items(self):
        order = Order()
        order.add_item(self._create_item("Product 1", 10, 1))
        order.add_item(self._create_item("Product 2", 20, 2))
        order.add_item(self._create_item("Product 3", 30, 3))
        assert len(order.items) == 3
    
    def test_remove_item(self):
        order = Order()
        item = self._create_item()
        order.add_item(item)
        order.remove_item(item.id)
        assert len(order.items) == 0
    
    def test_remove_nonexistent_item(self):
        order = Order()
        order.add_item(self._create_item())
        order.remove_item(uuid4())
        assert len(order.items) == 1
    
    def test_cannot_add_item_to_confirmed_order(self):
        order = Order()
        order.add_item(self._create_item())
        order.confirm()
        new_item = self._create_item("New Product", 50, 1)
        with pytest.raises(CannotModifyOrderError):
            order.add_item(new_item)
    
    def test_cannot_remove_item_from_confirmed_order(self):
        order = Order()
        order.add_item(self._create_item())
        order.confirm()
        item_id = order.items[0].id
        with pytest.raises(CannotModifyOrderError):
            order.remove_item(item_id)


class TestOrderTotalAmount:
    """Tests for Order total amount calculation."""
    
    def test_empty_order_total_is_zero(self):
        order = Order()
        assert order.total_amount.amount == 0
    
    def test_total_with_single_item(self):
        order = Order()
        order.add_item(OrderItem(
            product_name="Product",
            unit_price=Money.create(10.00, "USD"),
            quantity=Quantity.create(2),
        ))
        assert order.total_amount.amount == 20.00
    
    def test_total_with_multiple_items(self):
        order = Order()
        order.add_item(OrderItem(
            product_name="Product 1",
            unit_price=Money.create(10.00, "USD"),
            quantity=Quantity.create(2),
        ))
        order.add_item(OrderItem(
            product_name="Product 2",
            unit_price=Money.create(15.00, "USD"),
            quantity=Quantity.create(3),
        ))
        assert order.total_amount.amount == 65.00


class TestOrderItemCount:
    """Tests for Order item count."""
    
    def test_empty_order_item_count_is_zero(self):
        order = Order()
        assert order.item_count == 0
    
    def test_item_count_calculation(self):
        order = Order()
        order.add_item(OrderItem(
            product_name="Product 1",
            unit_price=Money.create(10.00, "USD"),
            quantity=Quantity.create(2),
        ))
        order.add_item(OrderItem(
            product_name="Product 2",
            unit_price=Money.create(15.00, "USD"),
            quantity=Quantity.create(3),
        ))
        assert order.item_count == 5


class TestOrderStatusTransitions:
    """Tests for Order status transitions."""
    
    def _create_order_with_items(self):
        order = Order()
        order.add_item(OrderItem(
            product_name="Test",
            unit_price=Money.create(10.0, "USD"),
            quantity=Quantity.create(1),
        ))
        return order
    
    def test_confirm_pending_order_with_items(self):
        order = self._create_order_with_items()
        order.confirm()
        assert order.status == OrderStatus.confirmed()
    
    def test_confirm_empty_order_raises_error(self):
        order = Order()
        with pytest.raises(EmptyOrderError):
            order.confirm()
    
    def test_confirm_already_confirmed_order_raises_error(self):
        order = self._create_order_with_items()
        order.confirm()
        with pytest.raises(InvalidOrderStatusTransitionError):
            order.confirm()
    
    def test_cancel_pending_order(self):
        order = self._create_order_with_items()
        order.cancel()
        assert order.status == OrderStatus.cancelled()
    
    def test_cancel_confirmed_order(self):
        order = self._create_order_with_items()
        order.confirm()
        order.cancel()
        assert order.status == OrderStatus.cancelled()
    
    def test_cancel_delivered_order_raises_error(self):
        order = self._create_order_with_items()
        order.confirm()
        order.update_status(OrderStatus.processing())
        order.update_status(OrderStatus.shipped())
        order.update_status(OrderStatus.delivered())
        with pytest.raises(InvalidOrderStatusTransitionError):
            order.cancel()
    
    def test_update_status_valid_transition(self):
        order = self._create_order_with_items()
        order.update_status(OrderStatus.confirmed())
        assert order.status == OrderStatus.confirmed()
    
    def test_update_status_invalid_transition(self):
        order = self._create_order_with_items()
        with pytest.raises(InvalidOrderStatusTransitionError):
            order.update_status(OrderStatus.shipped())


class TestOrderEquality:
    """Tests for Order equality (by ID)."""
    
    def test_different_id_orders_not_equal(self):
        order1 = Order()
        order2 = Order()
        assert order1 != order2
        assert order1.id != order2.id
