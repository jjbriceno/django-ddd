"""Order Entity - Aggregate root for orders"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID

from .base import BaseEntity
from .order_item import OrderItem
from ..value_objects import Money, OrderStatus, Quantity


@dataclass
class Order(BaseEntity):
    """Order aggregate root.
    
    DDD Principles demonstrated:
    - Aggregate root: Controls access to all OrderItems
    - Encapsulation: Business logic for modifying order state
    - Identity: Unique ID across the system
    - Consistency boundary: Ensures order items consistency
    """
    customer_id: UUID | None = None
    status: OrderStatus = field(default_factory=OrderStatus.pending)
    items: list[OrderItem] = field(default_factory=list)
    shipping_address: str = ""
    notes: str = ""

    def __post_init__(self) -> None:
        if self.status is None:
            self.status = OrderStatus.pending()

    @property
    def total_amount(self) -> Money:
        total = Money.zero("USD")
        for item in self.items:
            total = total.add(item.total_price)
        return total

    @property
    def item_count(self) -> int:
        return sum(item.quantity.value for item in self.items if item.quantity)

    def add_item(self, item: OrderItem) -> None:
        if self.status != OrderStatus.pending():
            raise ValueError("Can only add items to pending orders")
        self.items.append(item)
        self.updated_at = datetime.now()

    def remove_item(self, item_id: UUID) -> None:
        if self.status != OrderStatus.pending():
            raise ValueError("Can only remove items from pending orders")
        self.items = [item for item in self.items if item.id != item_id]
        self.updated_at = datetime.now()

    def confirm(self) -> None:
        if not self.items:
            raise ValueError("Cannot confirm order without items")
        new_status = OrderStatus.confirmed()
        if not self.status.can_transition_to(new_status):
            raise ValueError(f"Cannot transition from {self.status} to {new_status}")
        self.status = new_status
        self.updated_at = datetime.now()

    def cancel(self) -> None:
        new_status = OrderStatus.cancelled()
        if not self.status.can_transition_to(new_status):
            raise ValueError(f"Cannot transition from {self.status} to {new_status}")
        self.status = new_status
        self.updated_at = datetime.now()

    def update_status(self, new_status: OrderStatus) -> None:
        if not self.status.can_transition_to(new_status):
            raise ValueError(
                f"Invalid transition from {self.status.value} to {new_status.value}"
            )
        self.status = new_status
        self.updated_at = datetime.now()