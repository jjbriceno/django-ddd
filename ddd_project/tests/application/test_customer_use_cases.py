"""Tests for Customer use cases.

Application Layer Testing Principles:
- Test use cases in isolation with mocked repositories
- Test both success and failure scenarios
"""
import pytest
from uuid import uuid4

from ddd_project.apps.application.services.customers import (
    CreateCustomerUseCase,
    GetCustomerUseCase,
    ListCustomersUseCase,
)
from ddd_project.apps.application.dtos import CustomerCreateDTO, AddressDTO
from ddd_project.apps.domain.entities import Customer
from ddd_project.apps.domain.value_objects import Address


class TestCreateCustomerUseCase:
    """Tests for CreateCustomerUseCase."""
    
    def test_execute_creates_customer_successfully(self, mock_customer_repository):
        use_case = CreateCustomerUseCase(mock_customer_repository)
        dto = CustomerCreateDTO(
            name="John Doe",
            email="john@example.com",
            address=AddressDTO(
                street="123 Main St",
                city="New York",
                state="NY",
                postal_code="10001",
                country="USA",
            ),
        )
        result = use_case.execute(dto)
        assert result is not None
        assert result.name == "John Doe"
        assert result.email == "john@example.com"
    
    def test_execute_saves_customer_to_repository(self, mock_customer_repository):
        use_case = CreateCustomerUseCase(mock_customer_repository)
        dto = CustomerCreateDTO(
            name="Jane Doe",
            email="jane@example.com",
            address=AddressDTO(
                street="456 Oak Ave",
                city="Los Angeles",
                state="CA",
                postal_code="90001",
                country="USA",
            ),
        )
        use_case.execute(dto)
        customers = mock_customer_repository.find_all()
        assert len(customers) == 1
        assert customers[0].name == "Jane Doe"


class TestGetCustomerUseCase:
    """Tests for GetCustomerUseCase."""
    
    def test_execute_returns_customer_when_found(self, mock_customer_repository):
        customer = Customer(
            name="John Doe",
            email="john@example.com",
        )
        mock_customer_repository.save(customer)
        use_case = GetCustomerUseCase(mock_customer_repository)
        result = use_case.execute(customer.id)
        assert result is not None
        assert result.name == "John Doe"
    
    def test_execute_returns_none_when_not_found(self, mock_customer_repository):
        use_case = GetCustomerUseCase(mock_customer_repository)
        result = use_case.execute(uuid4())
        assert result is None


class TestListCustomersUseCase:
    """Tests for ListCustomersUseCase."""
    
    def test_execute_returns_empty_list_when_no_customers(self, mock_customer_repository):
        use_case = ListCustomersUseCase(mock_customer_repository)
        result = use_case.execute()
        assert result == []
    
    def test_execute_returns_all_customers(self, mock_customer_repository):
        c1 = Customer(name="Customer 1", email="c1@example.com")
        c2 = Customer(name="Customer 2", email="c2@example.com")
        mock_customer_repository.save(c1)
        mock_customer_repository.save(c2)
        use_case = ListCustomersUseCase(mock_customer_repository)
        result = use_case.execute()
        assert len(result) == 2
