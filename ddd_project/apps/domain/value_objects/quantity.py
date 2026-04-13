"""Quantity Value Object - Immutable positive integer"""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Quantity:
    """Immutable value object representing a positive integer quantity.
    
    DDD Principles demonstrated:
    - Immutable: uses frozen dataclass
    - Self-validating: enforces positive values only
    - Value equality: same values are equal
    """
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("Quantity must be non-negative")
        if not isinstance(self.value, int):
            raise ValueError("Quantity must be an integer")

    @classmethod
    def create(cls, value: int) -> Quantity:
        if not isinstance(value, int):
            raise ValueError("Quantity must be an integer")
        if value < 0:
            raise ValueError("Quantity must be non-negative")
        return cls(value)

    @classmethod
    def zero(cls) -> Quantity:
        return cls(0)

    def add(self, other: Quantity) -> Quantity:
        return Quantity(self.value + other.value)

    def subtract(self, other: Quantity) -> Quantity:
        result = self.value - other.value
        if result < 0:
            raise ValueError("Resulting quantity cannot be negative")
        return Quantity(result)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Quantity):
            return NotImplemented
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return f"Quantity({self.value})"

    def __int__(self) -> int:
        return self.value