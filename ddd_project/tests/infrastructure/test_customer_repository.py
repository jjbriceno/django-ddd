"""Tests for DjangoCustomerRepository.

Infrastructure Layer Testing Principles:
- Test with actual Django ORM using in-memory SQLite database
- Test persistence mapping between domain and ORM
- Test CRUD operations
"""
import pytest
from uuid import uuid4

from ddd_project.apps.infrastructure.repositories import DjangoCustomerRepository
from ddd_project.apps.domain.entities import Customer
from ddd_project.apps.domain.value_objects import Address


@pytest.mark.django_db(transaction=True)
class TestDjangoCustomerRepository:
    """Tests for DjangoCustomerRepository with actual database."""
    
    def _create_customer(self, name="John Doe", email="john@example.com"):
        return Customer(
            name=name,
            email=email,
            address=Address.create(
                street="123 Main St",
                city="New York",
                state="NY",
                postal_code="10001",
                country="USA",
            ),
        )
    
    def test_save_creates_new_customer(self):
        repository = DjangoCustomerRepository()
        customer = self._create_customer()
        saved_customer = repository.save(customer)
        assert saved_customer.id == customer.id
    
    def test_save_updates_existing_customer(self):
        repository = DjangoCustomerRepository()
        customer = self._create_customer()
        repository.save(customer)
        customer.name = "Jane Doe"
        updated_customer = repository.save(customer)
        assert updated_customer.name == "Jane Doe"
    
    def test_find_by_id_returns_none_for_nonexistent(self):
        repository = DjangoCustomerRepository()
        found_customer = repository.find_by_id(uuid4())
        assert found_customer is None
    
    def test_find_all_returns_empty_list_when_no_customers(self):
        repository = DjangoCustomerRepository()
        all_customers = repository.find_all()
        assert all_customers == []
    
    def test_delete_returns_false_for_nonexistent(self):
        repository = DjangoCustomerRepository()
        result = repository.delete(uuid4())
        assert result is False
