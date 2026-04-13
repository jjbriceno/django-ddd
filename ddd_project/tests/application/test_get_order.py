"""Tests for GetOrderUseCase.

Application Layer Testing Principles:
- Test use cases in isolation with mocked repositories
- Test both success (order found) and failure (order not found) scenarios
"""
import pytest
from uuid import uuid4

from ddd_project.apps.application.services.orders import GetOrderUseCase
from ddd_project.apps.domain.entities import Order, OrderItem
from ddd_project.apps.domain.value_objects import Money, Quantity


class TestGetOrderUseCase:
    """Tests for GetOrderUseCase."""
    
    def _create_order_with_items(self):
        order = Order(shipping_address="123 Main St")
        order.add_item(OrderItem(
            product_name="Test Product",
            unit_price=Money.create(29.99, "USD"),
            quantity=Quantity.create(2),
        ))
        return order
    
    def test_execute_returns_order_when_found(self, mock_order_repository):
        order = self._create_order_with_items()
        mock_order_repository.save(order)
        use_case = GetOrderUseCase(mock_order_repository)
        result = use_case.execute(order.id)
        assert result is not None
        assert result.shipping_address == "123 Main St"
        assert len(result.items) == 1
    
    def test_execute_returns_none_when_not_found(self, mock_order_repository):
        use_case = GetOrderUseCase(mock_order_repository)
        result = use_case.execute(uuid4())
        assert result is None
    
    def test_execute_calls_repository_find_by_id(self, mock_order_repository):
        order = self._create_order_with_items()
        mock_order_repository.save(order)
        use_case = GetOrderUseCase(mock_order_repository)
        use_case.execute(order.id)
        assert len(mock_order_repository._find_calls) == 1
        assert mock_order_repository._find_calls[0] == order.id
