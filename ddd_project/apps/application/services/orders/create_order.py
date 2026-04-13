"""Use Case: Create Order"""
from ddd_project.apps.domain.repositories import OrderRepository
from ddd_project.apps.application.dtos import OrderCreateDTO, OrderResponseDTO
from ddd_project.apps.application.mappers import OrderMapper


class CreateOrderUseCase:
    """Use case: Create a new order."""
    
    def __init__(self, repository: OrderRepository):
        self._repository = repository

    def execute(self, dto: OrderCreateDTO) -> OrderResponseDTO:
        order = OrderMapper.to_domain(dto)
        saved_order = self._repository.save(order)
        return OrderMapper.to_dto(saved_order)