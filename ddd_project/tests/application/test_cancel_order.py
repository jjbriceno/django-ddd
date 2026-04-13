"""Tests for CancelOrderUseCase.

Application Layer Testing Principles:
- Test use cases in isolation with mocked repositories
- Test status transition behavior
"""
import pytest

from ddd_project.apps.application.services.orders import CancelOrderUseCase
from ddd_project.apps.domain.entities import Order, OrderItem
from ddd_project.apps.domain.value_objects import Money, Quantity


class TestCancelOrderUseCase:
    """Tests for CancelOrderUseCase."""
    
    def _create_order_with_items(self):
        order = Order(shipping_address="123 Main St")
        order.add_item(OrderItem(
            product_name="Test Product",
            unit_price=Money.create(29.99, "USD"),
            quantity=Quantity.create(2),
        ))
        return order
    
    def test_execute_cancels_order_successfully(self, mock_order_repository):
        order = self._create_order_with_items()
        mock_order_repository.save(order)
        use_case = CancelOrderUseCase(mock_order_repository)
        result = use_case.execute(order.id)
        assert result is not None
        assert result.status == "CANCELLED"
    
    def test_execute_returns_none_when_order_not_found(self, mock_order_repository):
        from uuid import uuid4
        use_case = CancelOrderUseCase(mock_order_repository)
        result = use_case.execute(uuid4())
        assert result is None
    
    def test_execute_saves_cancelled_order(self, mock_order_repository):
        order = self._create_order_with_items()
        mock_order_repository.save(order)
        use_case = CancelOrderUseCase(mock_order_repository)
        use_case.execute(order.id)
        saved_order = mock_order_repository.get_saved_order()
        assert saved_order.status.value.value == "CANCELLED"
