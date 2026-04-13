"""Tests for CreateOrderUseCase.

Application Layer Testing Principles:
- Test use cases in isolation with mocked repositories
- Verify correct repository calls with expected parameters
- Verify DTO transformation
- Test both success and failure scenarios
"""
import pytest
from uuid import uuid4

from ddd_project.apps.application.services.orders import CreateOrderUseCase
from ddd_project.apps.application.dtos import OrderCreateDTO, OrderItemDTO


class TestCreateOrderUseCase:
    """Tests for CreateOrderUseCase."""
    
    def test_execute_creates_order_successfully(self, mock_order_repository):
        use_case = CreateOrderUseCase(mock_order_repository)
        dto = OrderCreateDTO(
            items=[
                OrderItemDTO(product_name="Test Product", unit_price=29.99, quantity=2),
            ],
            shipping_address="123 Main St, New York, NY 10001",
        )
        result = use_case.execute(dto)
        assert result is not None
        assert result.shipping_address == "123 Main St, New York, NY 10001"
        assert len(result.items) == 1
        assert result.status == "PENDING"
        assert mock_order_repository.was_saved()
    
    def test_execute_with_multiple_items(self, mock_order_repository):
        use_case = CreateOrderUseCase(mock_order_repository)
        dto = OrderCreateDTO(
            items=[
                OrderItemDTO(product_name="Product 1", unit_price=10.00, quantity=2),
                OrderItemDTO(product_name="Product 2", unit_price=20.00, quantity=1),
                OrderItemDTO(product_name="Product 3", unit_price=15.00, quantity=3),
            ],
            shipping_address="123 Main St",
        )
        result = use_case.execute(dto)
        assert len(result.items) == 3
        assert result.item_count == 6
        assert result.total_amount == 85.0
    
    def test_execute_with_customer_id(self, mock_order_repository):
        use_case = CreateOrderUseCase(mock_order_repository)
        customer_id = uuid4()
        dto = OrderCreateDTO(
            customer_id=customer_id,
            items=[
                OrderItemDTO(product_name="Test Product", unit_price=29.99, quantity=1),
            ],
            shipping_address="123 Main St",
        )
        result = use_case.execute(dto)
        assert result.customer_id == customer_id
    
    def test_execute_saves_order_to_repository(self, mock_order_repository):
        use_case = CreateOrderUseCase(mock_order_repository)
        dto = OrderCreateDTO(
            items=[
                OrderItemDTO(product_name="Test Product", unit_price=29.99, quantity=1),
            ],
            shipping_address="123 Main St",
        )
        use_case.execute(dto)
        saved_order = mock_order_repository.get_saved_order()
        assert saved_order is not None
        assert saved_order.shipping_address == "123 Main St"
