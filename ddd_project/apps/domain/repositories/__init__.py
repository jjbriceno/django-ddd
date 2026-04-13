"""Repository Interfaces - Domain Layer"""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities import Order, Customer


class OrderRepository(ABC):
    """Repository interface for Order aggregate.
    
    DDD Principles demonstrated:
    - Abstraction: Defines contract without implementation
    - Interface segregation: Clear contract for persistence
    - Dependency inversion: Domain defines what it needs
    """

    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def find_by_id(self, order_id: UUID) -> Optional[Order]:
        pass

    @abstractmethod
    def find_all(self) -> list[Order]:
        pass

    @abstractmethod
    def delete(self, order_id: UUID) -> bool:
        pass


class CustomerRepository(ABC):
    """Repository interface for Customer entity."""

    @abstractmethod
    def save(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    def find_by_id(self, customer_id: UUID) -> Optional[Customer]:
        pass

    @abstractmethod
    def find_all(self) -> list[Customer]:
        pass

    @abstractmethod
    def delete(self, customer_id: UUID) -> bool:
        pass