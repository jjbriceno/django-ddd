"""Tests for DjangoOrderRepository.

Infrastructure Layer Testing Principles:
- Test with actual Django ORM using in-memory SQLite database
- Test persistence mapping between domain and ORM
- Test CRUD operations
"""
import pytest
from uuid import uuid4

from ddd_project.apps.infrastructure.repositories import DjangoOrderRepository
from ddd_project.apps.domain.entities import Order, OrderItem
from ddd_project.apps.domain.value_objects import Money, Quantity, OrderStatus


@pytest.mark.django_db
class TestDjangoOrderRepository:
    """Tests for DjangoOrderRepository with actual database."""
    
    def _create_order_with_items(self):
        order = Order(shipping_address="123 Main St, New York, NY 10001")
        order.add_item(OrderItem(
            product_name="Test Product",
            unit_price=Money.create(29.99, "USD"),
            quantity=Quantity.create(2),
        ))
        order.add_item(OrderItem(
            product_name="Another Product",
            unit_price=Money.create(49.99, "USD"),
            quantity=Quantity.create(1),
        ))
        return order
    
    def test_save_creates_new_order(self):
        repository = DjangoOrderRepository()
        order = self._create_order_with_items()
        saved_order = repository.save(order)
        assert saved_order.id == order.id
    
    def test_save_updates_existing_order(self):
        repository = DjangoOrderRepository()
        order = self._create_order_with_items()
        repository.save(order)
        order.shipping_address = "456 New St, Los Angeles, CA 90001"
        updated_order = repository.save(order)
        assert updated_order.shipping_address == "456 New St, Los Angeles, CA 90001"
    
    def test_find_by_id_returns_order(self):
        repository = DjangoOrderRepository()
        order = self._create_order_with_items()
        repository.save(order)
        found_order = repository.find_by_id(order.id)
        assert found_order is not None
        assert found_order.id == order.id
        assert found_order.shipping_address == order.shipping_address
    
    def test_find_by_id_returns_none_for_nonexistent(self):
        repository = DjangoOrderRepository()
        found_order = repository.find_by_id(uuid4())
        assert found_order is None
    
    def test_find_all_returns_all_orders(self):
        repository = DjangoOrderRepository()
        order1 = self._create_order_with_items()
        order2 = Order(shipping_address="Another Address")
        order2.add_item(OrderItem(
            product_name="Product",
            unit_price=Money.create(10.00, "USD"),
            quantity=Quantity.create(1),
        ))
        repository.save(order1)
        repository.save(order2)
        all_orders = repository.find_all()
        assert len(all_orders) == 2
    
    def test_find_all_returns_empty_list_when_no_orders(self):
        repository = DjangoOrderRepository()
        all_orders = repository.find_all()
        assert all_orders == []
    
    def test_delete_removes_order(self):
        repository = DjangoOrderRepository()
        order = self._create_order_with_items()
        repository.save(order)
        result = repository.delete(order.id)
        assert result is True
        assert repository.find_by_id(order.id) is None
    
    def test_delete_returns_false_for_nonexistent(self):
        repository = DjangoOrderRepository()
        result = repository.delete(uuid4())
        assert result is False
    
    def test_saved_order_preserves_items(self):
        repository = DjangoOrderRepository()
        order = self._create_order_with_items()
        repository.save(order)
        found_order = repository.find_by_id(order.id)
        assert len(found_order.items) == 2
        assert found_order.items[0].product_name == "Test Product"
        assert found_order.items[0].quantity.value == 2
    
    def test_saved_order_preserves_status(self):
        repository = DjangoOrderRepository()
        order = self._create_order_with_items()
        order.confirm()
        repository.save(order)
        found_order = repository.find_by_id(order.id)
        assert found_order.status == OrderStatus.confirmed()
