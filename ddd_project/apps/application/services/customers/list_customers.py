"""Use Case: List Customers"""
from ddd_project.apps.domain.repositories import CustomerRepository
from ddd_project.apps.application.dtos import CustomerResponseDTO
from ddd_project.apps.application.mappers import CustomerMapper


class ListCustomersUseCase:
    """Use case: List all customers."""
    
    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def execute(self) -> list[CustomerResponseDTO]:
        customers = self._repository.find_all()
        return CustomerMapper.to_dto_list(customers)