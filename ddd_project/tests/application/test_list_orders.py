"""Tests for ListOrdersUseCase.

Application Layer Testing Principles:
- Test use cases in isolation with mocked repositories
- Test empty list and populated list scenarios
"""
import pytest

from ddd_project.apps.application.services.orders import ListOrdersUseCase
from ddd_project.apps.domain.entities import Order, OrderItem
from ddd_project.apps.domain.value_objects import Money, Quantity


class TestListOrdersUseCase:
    """Tests for ListOrdersUseCase."""
    
    def _create_order(self, shipping_address="123 Main St"):
        order = Order(shipping_address=shipping_address)
        order.add_item(OrderItem(
            product_name="Test Product",
            unit_price=Money.create(10.00, "USD"),
            quantity=Quantity.create(1),
        ))
        return order
    
    def test_execute_returns_empty_list_when_no_orders(self, mock_order_repository):
        use_case = ListOrdersUseCase(mock_order_repository)
        result = use_case.execute()
        assert result == []
    
    def test_execute_returns_all_orders(self, mock_order_repository):
        order1 = self._create_order("Address 1")
        order2 = self._create_order("Address 2")
        mock_order_repository.save(order1)
        mock_order_repository.save(order2)
        use_case = ListOrdersUseCase(mock_order_repository)
        result = use_case.execute()
        assert len(result) == 2
    
    def test_execute_returns_correct_order_data(self, mock_order_repository):
        order = self._create_order("456 Oak Ave")
        mock_order_repository.save(order)
        use_case = ListOrdersUseCase(mock_order_repository)
        result = use_case.execute()
        assert result[0].shipping_address == "456 Oak Ave"
