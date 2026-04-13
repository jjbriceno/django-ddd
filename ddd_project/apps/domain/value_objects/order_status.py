"""OrderStatus Value Object - Immutable order state"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Final

from ddd_project.apps.domain.exceptions import InvalidOrderStatusError


class OrderStatusEnum(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


VALID_TRANSITIONS: Final = {
    OrderStatusEnum.PENDING: {OrderStatusEnum.CONFIRMED, OrderStatusEnum.CANCELLED},
    OrderStatusEnum.CONFIRMED: {OrderStatusEnum.PROCESSING, OrderStatusEnum.CANCELLED},
    OrderStatusEnum.PROCESSING: {OrderStatusEnum.SHIPPED, OrderStatusEnum.CANCELLED},
    OrderStatusEnum.SHIPPED: {OrderStatusEnum.DELIVERED, OrderStatusEnum.CANCELLED},
    OrderStatusEnum.DELIVERED: set(),
    OrderStatusEnum.CANCELLED: set(),
}


@dataclass(frozen=True, slots=True)
class OrderStatus:
    """Immutable value object representing order status."""
    value: OrderStatusEnum

    def __post_init__(self) -> None:
        if not isinstance(self.value, OrderStatusEnum):
            raise InvalidOrderStatusError(self.value)

    @classmethod
    def pending(cls) -> OrderStatus:
        return cls(OrderStatusEnum.PENDING)

    @classmethod
    def confirmed(cls) -> OrderStatus:
        return cls(OrderStatusEnum.CONFIRMED)

    @classmethod
    def processing(cls) -> OrderStatus:
        return cls(OrderStatusEnum.PROCESSING)

    @classmethod
    def shipped(cls) -> OrderStatus:
        return cls(OrderStatusEnum.SHIPPED)

    @classmethod
    def delivered(cls) -> OrderStatus:
        return cls(OrderStatusEnum.DELIVERED)

    @classmethod
    def cancelled(cls) -> OrderStatus:
        return cls(OrderStatusEnum.CANCELLED)

    @classmethod
    def from_string(cls, status: str) -> OrderStatus:
        try:
            return cls(OrderStatusEnum(status))
        except ValueError:
            raise InvalidOrderStatusError(status)

    def can_transition_to(self, new_status: OrderStatus) -> bool:
        return new_status.value in VALID_TRANSITIONS.get(self.value, set())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OrderStatus):
            return NotImplemented
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return self.value.value

    def __repr__(self) -> str:
        return f"OrderStatus({self.value.value})"