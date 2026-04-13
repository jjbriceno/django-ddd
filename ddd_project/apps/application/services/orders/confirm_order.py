"""Use Case: Confirm Order"""
from typing import Optional
from uuid import UUID

from ddd_project.apps.domain.repositories import OrderRepository
from ddd_project.apps.application.dtos import OrderResponseDTO
from ddd_project.apps.application.mappers import OrderMapper


class ConfirmOrderUseCase:
    """Use case: Confirm an order."""
    
    def __init__(self, repository: OrderRepository):
        self._repository = repository

    def execute(self, order_id: UUID) -> Optional[OrderResponseDTO]:
        order = self._repository.find_by_id(order_id)
        if order is None:
            return None

        order.confirm()
        confirmed_order = self._repository.save(order)
        return OrderMapper.to_dto(confirmed_order)