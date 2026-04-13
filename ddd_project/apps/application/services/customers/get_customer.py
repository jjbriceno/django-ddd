"""Use Case: Get Customer"""
from typing import Optional
from uuid import UUID

from ddd_project.apps.domain.repositories import CustomerRepository
from ddd_project.apps.application.dtos import CustomerResponseDTO
from ddd_project.apps.application.mappers import CustomerMapper


class GetCustomerUseCase:
    """Use case: Get customer by ID."""
    
    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def execute(self, customer_id: UUID) -> Optional[CustomerResponseDTO]:
        customer = self._repository.find_by_id(customer_id)
        if customer is None:
            return None
        return CustomerMapper.to_dto(customer)