"""Pytest configuration and shared fixtures for DDD tests.

This module demonstrates DDD testing principles:
- Domain tests: Pure unit tests, no dependencies
- Application tests: Tests use cases with mocked repositories
- Infrastructure tests: Tests with in-memory or test database
- Integration tests: Full stack API tests
"""
import os
import sys
from decimal import Decimal
from uuid import uuid4

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()


@pytest.fixture
def money_usd():
    """Factory fixture for USD money values."""
    def _create_money(amount: float | int | Decimal = 0) -> "Money":
        from ddd_project.apps.domain.value_objects import Money
        return Money.create(amount, "USD")
    return _create_money


@pytest.fixture
def money_eur():
    """Factory fixture for EUR money values."""
    def _create_money(amount: float | int | Decimal = 0) -> "Money":
        from ddd_project.apps.domain.value_objects import Money
        return Money.create(amount, "EUR")
    return _create_money


@pytest.fixture
def quantity():
    """Factory fixture for quantities."""
    def _create_quantity(value: int = 1) -> "Quantity":
        from ddd_project.apps.domain.value_objects import Quantity
        return Quantity.create(value)
    return _create_quantity


@pytest.fixture
def address():
    """Factory fixture for addresses."""
    def _create_address(
        street: str = "123 Main St",
        city: str = "New York",
        state: str = "NY",
        postal_code: str = "10001",
        country: str = "USA",
    ) -> "Address":
        from ddd_project.apps.domain.value_objects import Address
        return Address.create(street, city, state, postal_code, country)
    return _create_address


@pytest.fixture
def order_status():
    """Factory fixture for order statuses."""
    from ddd_project.apps.domain.value_objects import OrderStatus, OrderStatusEnum
    return {
        "pending": OrderStatus.pending,
        "confirmed": OrderStatus.confirmed,
        "processing": OrderStatus.processing,
        "shipped": OrderStatus.shipped,
        "delivered": OrderStatus.delivered,
        "cancelled": OrderStatus.cancelled,
    }


@pytest.fixture
def sample_order_item(money_usd, quantity):
    """Factory fixture for a sample order item."""
    def _create_item(
        product_name: str = "Test Product",
        unit_price: float = 29.99,
        qty: int = 2,
    ) -> "OrderItem":
        from ddd_project.apps.domain.entities import OrderItem
        return OrderItem(
            product_name=product_name,
            unit_price=money_usd(unit_price),
            quantity=quantity(qty),
        )
    return _create_item


@pytest.fixture
def sample_order(sample_order_item):
    """Factory fixture for a sample order with items."""
    def _create_order(with_items: bool = True) -> "Order":
        from ddd_project.apps.domain.entities import Order
        order = Order(shipping_address="123 Main St, New York, NY 10001")
        if with_items:
            order.add_item(sample_order_item())
            order.add_item(sample_order_item("Another Product", 49.99, 1))
        return order
    return _create_order


@pytest.fixture
def sample_customer(address):
    """Factory fixture for a sample customer."""
    def _create_customer(
        name: str = "John Doe",
        email: str = "john@example.com",
        with_address: bool = True,
    ) -> "Customer":
        from ddd_project.apps.domain.entities import Customer
        return Customer(
            name=name,
            email=email,
            address=address() if with_address else None,
        )
    return _create_customer


class MockOrderRepository:
    """In-memory mock implementation of OrderRepository for testing.
    
    This mock demonstrates:
    - Interface compliance through ABC
    - In-memory storage for fast tests
    - Easy state inspection for assertions
    """
    
    def __init__(self):
        self._orders: dict[uuid4, "Order"] = {}
        self._save_calls: list = []
        self._find_calls: list = []
    
    def save(self, order: "Order") -> "Order":
        self._save_calls.append(order)
        self._orders[order.id] = order
        return order
    
    def find_by_id(self, order_id) -> "Order | None":
        self._find_calls.append(order_id)
        return self._orders.get(order_id)
    
    def find_all(self) -> list["Order"]:
        return list(self._orders.values())
    
    def delete(self, order_id) -> bool:
        if order_id in self._orders:
            del self._orders[order_id]
            return True
        return False
    
    def was_saved(self) -> bool:
        return len(self._save_calls) > 0
    
    def get_saved_order(self) -> "Order | None":
        return self._save_calls[-1] if self._save_calls else None


class MockCustomerRepository:
    """In-memory mock implementation of CustomerRepository for testing."""
    
    def __init__(self):
        self._customers: dict[uuid4, "Customer"] = {}
        self._save_calls: list = []
    
    def save(self, customer: "Customer") -> "Customer":
        self._save_calls.append(customer)
        self._customers[customer.id] = customer
        return customer
    
    def find_by_id(self, customer_id) -> "Customer | None":
        return self._customers.get(customer_id)
    
    def find_all(self) -> list["Customer"]:
        return list(self._customers.values())
    
    def delete(self, customer_id) -> bool:
        if customer_id in self._customers:
            del self._customers[customer_id]
            return True
        return False


@pytest.fixture
def mock_order_repository():
    """Fixture providing a mock OrderRepository."""
    return MockOrderRepository()


@pytest.fixture
def mock_customer_repository():
    """Fixture providing a mock CustomerRepository."""
    return MockCustomerRepository()
