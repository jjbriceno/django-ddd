"""Use Case: Update Order Status"""
from typing import Optional
from uuid import UUID

from ddd_project.apps.domain.repositories import OrderRepository
from ddd_project.apps.domain.value_objects import OrderStatus
from ddd_project.apps.application.dtos import OrderUpdateStatusDTO, OrderResponseDTO
from ddd_project.apps.application.mappers import OrderMapper


class UpdateOrderStatusUseCase:
    """Use case: Update order status."""
    
    def __init__(self, repository: OrderRepository):
        self._repository = repository

    def execute(self, order_id: UUID, dto: OrderUpdateStatusDTO) -> Optional[OrderResponseDTO]:
        order = self._repository.find_by_id(order_id)
        if order is None:
            return None

        new_status = OrderStatus.from_string(dto.status)
        order.update_status(new_status)
        updated_order = self._repository.save(order)
        return OrderMapper.to_dto(updated_order)