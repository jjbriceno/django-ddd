"""Use Case: Create Customer"""
from ddd_project.apps.domain.repositories import CustomerRepository
from ddd_project.apps.application.dtos import CustomerCreateDTO, CustomerResponseDTO
from ddd_project.apps.application.mappers import CustomerMapper


class CreateCustomerUseCase:
    """Use case: Create a new customer."""
    
    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def execute(self, dto: CustomerCreateDTO) -> CustomerResponseDTO:
        customer = CustomerMapper.to_domain(dto)
        saved_customer = self._repository.save(customer)
        return CustomerMapper.to_dto(saved_customer)