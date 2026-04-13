"""Money Value Object - Immutable monetary value"""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Final

from ddd_project.apps.domain.exceptions import (
    InvalidCurrencyError,
    NegativeMoneyError,
    MoneyOperationError,
)


SUPPORTED_CURRENCIES: Final = {"USD", "EUR", "GBP"}


@dataclass(frozen=True, slots=True)
class Money:
    """Immutable value object representing monetary value."""
    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        if self.currency not in SUPPORTED_CURRENCIES:
            raise InvalidCurrencyError(self.currency)
        if self.amount < 0:
            raise NegativeMoneyError(self.amount)

    @classmethod
    def create(cls, amount: float | Decimal | int, currency: str) -> Money:
        return cls(Decimal(str(amount)), currency)

    @classmethod
    def zero(cls, currency: str = "USD") -> Money:
        return cls(Decimal("0"), currency)

    def add(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise MoneyOperationError("add")
        return Money(self.amount + other.amount, self.currency)

    def multiply(self, factor: Decimal | int | float) -> Money:
        return Money(self.amount * Decimal(str(factor)), self.currency)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency

    def __hash__(self) -> int:
        return hash((self.amount, self.currency))

    def __repr__(self) -> str:
        return f"Money({self.amount} {self.currency})"