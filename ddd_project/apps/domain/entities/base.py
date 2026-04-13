"""Base Entity - Abstract base class for domain entities"""
from __future__ import annotations
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import datetime


@dataclass
class BaseEntity:
    """Abstract base class for domain entities.
    
    DDD Principles demonstrated:
    - Identity: Each entity has a unique identifier
    - Equality: Entities are compared by identity, not attributes
    """
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseEntity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)