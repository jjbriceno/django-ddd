"""Address Value Object - Immutable postal address"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class Address:
    """Immutable value object representing a postal address.
    
    DDD Principles demonstrated:
    - Immutable: uses frozen dataclass
    - Self-validating: ensures required fields are present
    - Value equality: addresses with same values are equal
    """
    street: str
    city: str
    state: str
    postal_code: str
    country: str

    def __post_init__(self) -> None:
        if not self.street:
            raise ValueError("Street is required")
        if not self.city:
            raise ValueError("City is required")
        if not self.country:
            raise ValueError("Country is required")

    @classmethod
    def create(
        cls,
        street: str,
        city: str,
        state: str,
        postal_code: str,
        country: str,
    ) -> Address:
        return cls(
            street=street.strip(),
            city=city.strip(),
            state=state.strip() if state else "",
            postal_code=postal_code.strip(),
            country=country.strip(),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Address):
            return NotImplemented
        return (
            self.street == other.street
            and self.city == other.city
            and self.state == other.state
            and self.postal_code == other.postal_code
            and self.country == other.country
        )

    def __hash__(self) -> int:
        return hash(
            (self.street, self.city, self.state, self.postal_code, self.country)
        )

    def __repr__(self) -> str:
        return f"Address({self.street}, {self.city}, {self.country})"