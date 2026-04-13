"""OrderItem Entity - Entity within Order aggregate"""
from __future__ import annotations
from dataclasses import dataclass, field
from .base import BaseEntity
from ..value_objects import Money, Quantity


@dataclass
class OrderItem(BaseEntity):
    """Order item entity - part of Order aggregate.
    
    DDD Principles demonstrated:
    - Identity: Each item has unique ID
    - Lifecycle: Tied to parent aggregate
    - Value objects: Uses Money and Quantity
    """
    product_name: str = ""
    unit_price: Money | None = None
    quantity: Quantity | None = None

    def __post_init__(self) -> None:
        if not self.product_name:
            raise ValueError("Product name is required")
        if self.unit_price is None:
            raise ValueError("Unit price is required")
        if self.quantity is None:
            raise ValueError("Quantity is required")

    @property
    def total_price(self) -> Money:
        if self.unit_price is None or self.quantity is None:
            return Money.zero()
        return self.unit_price.multiply(self.quantity.value)