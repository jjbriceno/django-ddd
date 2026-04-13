"""Dependency Injection Container"""
from functools import lru_cache

from ddd_project.apps.domain.repositories import OrderRepository, CustomerRepository
from ddd_project.apps.infrastructure.repositories import (
    DjangoOrderRepository,
    DjangoCustomerRepository,
)
from ddd_project.apps.application.services import OrderService, CustomerService


class Container:
    """Simple dependency injection container.
    
    DI Principles:
    - Centralized wiring of dependencies
    - Interfaces over implementations
    - Easy to swap implementations
    """
    
    @staticmethod
    @lru_cache(maxsize=1)
    def get_order_repository() -> OrderRepository:
        return DjangoOrderRepository()

    @staticmethod
    @lru_cache(maxsize=1)
    def get_customer_repository() -> CustomerRepository:
        return DjangoCustomerRepository()

    @staticmethod
    def get_order_service() -> OrderService:
        return OrderService(Container.get_order_repository())

    @staticmethod
    def get_customer_service() -> CustomerService:
        return CustomerService(Container.get_customer_repository())


@lru_cache
def get_order_service() -> OrderService:
    """Factory function for OrderService - enables Django Ninja DI."""
    return Container.get_order_service()


@lru_cache
def get_customer_service() -> CustomerService:
    """Factory function for CustomerService - enables Django Ninja DI."""
    return Container.get_customer_service()