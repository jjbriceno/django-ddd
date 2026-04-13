"""Tests for ConfirmOrderUseCase.

Application Layer Testing Principles:
- Test use cases in isolation with mocked repositories
- Test business rule enforcement (order must have items)
- Test status transition behavior
"""
import pytest

from ddd_project.apps.application.services.orders import ConfirmOrderUseCase
from ddd_project.apps.domain.entities import Order, OrderItem
from ddd_project.apps.domain.value_objects import Money, Quantity


class TestConfirmOrderUseCase:
    """Tests for ConfirmOrderUseCase."""
    
    def _create_order_with_items(self):
        order = Order(shipping_address="123 Main St")
        order.add_item(OrderItem(
            product_name="Test Product",
            unit_price=Money.create(29.99, "USD"),
            quantity=Quantity.create(2),
        ))
        return order
    
    def test_execute_confirms_order_successfully(self, mock_order_repository):
        order = self._create_order_with_items()
        mock_order_repository.save(order)
        use_case = ConfirmOrderUseCase(mock_order_repository)
        result = use_case.execute(order.id)
        assert result is not None
        assert result.status == "CONFIRMED"
    
    def test_execute_returns_none_when_order_not_found(self, mock_order_repository):
        from uuid import uuid4
        use_case = ConfirmOrderUseCase(mock_order_repository)
        result = use_case.execute(uuid4())
        assert result is None
    
    def test_execute_saves_confirmed_order(self, mock_order_repository):
        order = self._create_order_with_items()
        mock_order_repository.save(order)
        use_case = ConfirmOrderUseCase(mock_order_repository)
        use_case.execute(order.id)
        saved_order = mock_order_repository.get_saved_order()
        assert saved_order.status.value.value == "CONFIRMED"
    
    def test_execute_updates_order_in_repository(self, mock_order_repository):
        order = self._create_order_with_items()
        mock_order_repository.save(order)
        initial_updated_at = order.updated_at
        use_case = ConfirmOrderUseCase(mock_order_repository)
        use_case.execute(order.id)
        assert mock_order_repository.get_saved_order().updated_at >= initial_updated_at
