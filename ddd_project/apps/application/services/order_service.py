"""Order Service - Application service for order operations"""
from typing import Optional
from uuid import UUID

from ddd_project.apps.domain.entities import Order
from ddd_project.apps.domain.repositories import OrderRepository
from ddd_project.apps.domain.value_objects import OrderStatus
from ddd_project.apps.application.dtos import (
    OrderCreateDTO,
    OrderResponseDTO,
    OrderUpdateStatusDTO,
)
from ddd_project.apps.application.mappers import OrderMapper


class OrderService:
    """Application service for order use cases.
    
    Service Principles:
    - Orchestrates domain operations
    - Uses repositories for persistence
    - Converts DTOs via mappers
    - Implements use cases
    """
    
    def __init__(self, repository: OrderRepository):
        self._repository = repository

    def create_order(self, dto: OrderCreateDTO) -> OrderResponseDTO:
        """Use case: Create a new order."""
        order = OrderMapper.to_domain(dto)
        saved_order = self._repository.save(order)
        return OrderMapper.to_dto(saved_order)

    def get_order(self, order_id: UUID) -> Optional[OrderResponseDTO]:
        """Use case: Get order by ID."""
        order = self._repository.find_by_id(order_id)
        if order is None:
            return None
        return OrderMapper.to_dto(order)

    def list_orders(self) -> list[OrderResponseDTO]:
        """Use case: List all orders."""
        orders = self._repository.find_all()
        return OrderMapper.to_dto_list(orders)

    def update_status(
        self, order_id: UUID, dto: OrderUpdateStatusDTO
    ) -> Optional[OrderResponseDTO]:
        """Use case: Update order status."""
        order = self._repository.find_by_id(order_id)
        if order is None:
            return None

        new_status = OrderStatus.from_string(dto.status)
        order.update_status(new_status)
        updated_order = self._repository.save(order)
        return OrderMapper.to_dto(updated_order)

    def confirm_order(self, order_id: UUID) -> Optional[OrderResponseDTO]:
        """Use case: Confirm an order."""
        order = self._repository.find_by_id(order_id)
        if order is None:
            return None

        order.confirm()
        confirmed_order = self._repository.save(order)
        return OrderMapper.to_dto(confirmed_order)

    def cancel_order(self, order_id: UUID) -> Optional[OrderResponseDTO]:
        """Use case: Cancel an order."""
        order = self._repository.find_by_id(order_id)
        if order is None:
            return None

        order.cancel()
        cancelled_order = self._repository.save(order)
        return OrderMapper.to_dto(cancelled_order)