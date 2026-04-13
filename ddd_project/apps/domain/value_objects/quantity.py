"""Quantity Value Object - Immutable positive integer"""
from __future__ import annotations
from dataclasses import dataclass

from ddd_project.apps.domain.exceptions import (
    InvalidQuantityError,
    NegativeQuantityError,
)


@dataclass(frozen=True, slots=True)
class Quantity:
    """Immutable value object representing a positive integer quantity."""
    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise InvalidQuantityError(self.value)
        if self.value < 0:
            raise NegativeQuantityError(self.value)

    @classmethod
    def create(cls, value: int) -> Quantity:
        if not isinstance(value, int):
            raise InvalidQuantityError(value)
        if value < 0:
            raise NegativeQuantityError(value)
        return cls(value)

    @classmethod
    def zero(cls) -> Quantity:
        return cls(0)

    def add(self, other: Quantity) -> Quantity:
        return Quantity(self.value + other.value)

    def subtract(self, other: Quantity) -> Quantity:
        result = self.value - other.value
        if result < 0:
            raise NegativeQuantityError(result)
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