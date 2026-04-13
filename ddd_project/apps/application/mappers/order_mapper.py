"""Order Mapper - Converts between domain entities and DTOs"""
from typing import Optional
from uuid import UUID

from ddd_project.apps.domain.entities import Order, OrderItem
from ddd_project.apps.domain.value_objects import Money, OrderStatus, Quantity
from ddd_project.apps.application.dtos import (
    OrderCreateDTO,
    OrderResponseDTO,
    OrderItemDTO,
    OrderItemResponseDTO,
    OrderUpdateStatusDTO,
)


class OrderMapper:
    """Maps between Order domain entity and DTOs.
    
    Mapper Principles:
    - Isolates conversion logic from domain
    - Converts DTOs to domain entities
    - Converts domain entities to DTOs
    - Single responsibility for conversion
    """

    @staticmethod
    def to_domain(dto: OrderCreateDTO, order_id: Optional[UUID] = None) -> Order:
        """Convert CreateDTO to Order domain entity."""
        order = Order()
        if order_id:
            order.id = order_id
        order.customer_id = dto.customer_id
        order.shipping_address = dto.shipping_address
        order.notes = dto.notes
        order.status = OrderStatus.pending()

        for item_dto in dto.items:
            order.items.append(
                OrderItem(
                    product_name=item_dto.product_name,
                    unit_price=Money.create(item_dto.unit_price, "USD"),
                    quantity=Quantity.create(item_dto.quantity),
                )
            )

        return order

    @staticmethod
    def to_dto(order: Order) -> OrderResponseDTO:
        """Convert Order domain entity to ResponseDTO."""
        items = []
        for item in order.items:
            items.append(
                OrderItemResponseDTO(
                    id=item.id,
                    product_name=item.product_name,
                    unit_price=float(item.unit_price.amount),
                    quantity=item.quantity.value,
                    total_price=float(item.total_price.amount),
                )
            )

        return OrderResponseDTO(
            id=order.id,
            customer_id=order.customer_id,
            status=str(order.status),
            items=items,
            total_amount=float(order.total_amount.amount),
            item_count=order.item_count,
            shipping_address=order.shipping_address,
            notes=order.notes,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )

    @staticmethod
    def to_dto_list(orders: list[Order]) -> list[OrderResponseDTO]:
        """Convert list of orders to list of DTOs."""
        return [OrderMapper.to_dto(order) for order in orders]