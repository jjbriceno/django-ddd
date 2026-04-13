"""Customer Entity - Domain entity representing a customer"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from .base import BaseEntity
from ..value_objects import Address


@dataclass
class Customer(BaseEntity):
    """Customer entity with identity and address.
    
    DDD Principles demonstrated:
    - Identity: Unique ID generated on creation
    - Encapsulation: Mutable state with controlled changes
    - Value objects: Uses Address value object
    """
    name: str = ""
    email: str = ""
    address: Address | None = None
    is_active: bool = True

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Customer name is required")
        if not self.email:
            raise ValueError("Customer email is required")

    def update_address(self, new_address: Address) -> None:
        self.address = new_address
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now()

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.now()