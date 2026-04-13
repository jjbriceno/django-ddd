"""Customer Service - Application service for customer operations"""
from typing import Optional
from uuid import UUID

from ddd_project.apps.domain.entities import Customer
from ddd_project.apps.domain.repositories import CustomerRepository
from ddd_project.apps.application.dtos import (
    CustomerCreateDTO,
    CustomerResponseDTO,
)
from ddd_project.apps.application.mappers import CustomerMapper


class CustomerService:
    """Application service for customer use cases."""

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def create_customer(self, dto: CustomerCreateDTO) -> CustomerResponseDTO:
        """Use case: Create a new customer."""
        customer = CustomerMapper.to_domain(dto)
        saved_customer = self._repository.save(customer)
        return CustomerMapper.to_dto(saved_customer)

    def get_customer(self, customer_id: UUID) -> Optional[CustomerResponseDTO]:
        """Use case: Get customer by ID."""
        customer = self._repository.find_by_id(customer_id)
        if customer is None:
            return None
        return CustomerMapper.to_dto(customer)

    def list_customers(self) -> list[CustomerResponseDTO]:
        """Use case: List all customers."""
        customers = self._repository.find_all()
        return CustomerMapper.to_dto_list(customers)