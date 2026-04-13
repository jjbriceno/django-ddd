"""Use Case: List Orders"""
from ddd_project.apps.domain.repositories import OrderRepository
from ddd_project.apps.application.dtos import OrderResponseDTO
from ddd_project.apps.application.mappers import OrderMapper


class ListOrdersUseCase:
    """Use case: List all orders."""
    
    def __init__(self, repository: OrderRepository):
        self._repository = repository

    def execute(self) -> list[OrderResponseDTO]:
        orders = self._repository.find_all()
        return OrderMapper.to_dto_list(orders)