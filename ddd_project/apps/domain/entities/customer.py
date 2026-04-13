"""Customer Entity - Domain entity representing a customer"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

from .base import BaseEntity
from ..value_objects import Address
from ..exceptions import RequiredCustomerNameError, RequiredCustomerEmailError


@dataclass
class Customer(BaseEntity):
    """Customer entity with identity and address."""
    name: str = ""
    email: str = ""
    address: Address | None = None
    is_active: bool = True

    def __post_init__(self) -> None:
        if not self.name:
            raise RequiredCustomerNameError()
        if not self.email:
            raise RequiredCustomerEmailError()

    def update_address(self, new_address: Address) -> None:
        self.address = new_address
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now()

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.now()