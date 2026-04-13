"""Tests for Customer entity.

Domain Layer Testing Principles:
- Pure unit tests with no external dependencies
- Test entity creation, validation, and behavior
"""
import pytest

from ddd_project.apps.domain.entities import Customer
from ddd_project.apps.domain.exceptions import (
    RequiredCustomerNameError,
    RequiredCustomerEmailError,
)


class TestCustomerCreation:
    """Tests for Customer creation."""
    
    def test_create_valid_customer(self, sample_customer):
        customer = sample_customer()
        assert customer.id is not None
        assert customer.name == "John Doe"
        assert customer.email == "john@example.com"
        assert customer.is_active is True
        assert customer.address is not None
    
    def test_create_customer_without_address(self, sample_customer):
        customer = sample_customer(with_address=False)
        assert customer.address is None
    
    def test_empty_name_raises_error(self, address):
        with pytest.raises(RequiredCustomerNameError):
            Customer(name="", email="john@example.com", address=address())
    
    def test_empty_email_raises_error(self, address):
        with pytest.raises(RequiredCustomerEmailError):
            Customer(name="John", email="", address=address())
    
    def test_customer_has_timestamps(self):
        customer = Customer(
            name="Test User",
            email="test@example.com",
        )
        assert customer.created_at is not None
        assert customer.updated_at is not None


class TestCustomerAddressUpdate:
    """Tests for Customer address update."""
    
    def test_update_address(self, sample_customer, address):
        customer = sample_customer()
        new_address = address(
            street="456 New St",
            city="Los Angeles",
            state="CA",
            postal_code="90001",
            country="USA",
        )
        customer.update_address(new_address)
        assert customer.address == new_address
        assert customer.address.street == "456 New St"


class TestCustomerActivation:
    """Tests for Customer activation/deactivation."""
    
    def test_deactivate_customer(self, sample_customer):
        customer = sample_customer()
        assert customer.is_active is True
        customer.deactivate()
        assert customer.is_active is False
    
    def test_activate_customer(self, sample_customer):
        customer = sample_customer()
        customer.deactivate()
        assert customer.is_active is False
        customer.activate()
        assert customer.is_active is True


class TestCustomerEquality:
    """Tests for Customer equality (by ID)."""
    
    def test_different_id_customers_not_equal(self):
        c1 = Customer(name="A", email="a@example.com")
        c2 = Customer(name="A", email="a@example.com")
        assert c1 != c2
        assert c1.id != c2.id
