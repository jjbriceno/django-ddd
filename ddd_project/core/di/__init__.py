"""Dependency Injection Container"""
from functools import lru_cache

from ddd_project.apps.domain.repositories import OrderRepository, CustomerRepository
from ddd_project.apps.infrastructure.repositories import (
    DjangoOrderRepository,
    DjangoCustomerRepository,
)
from ddd_project.apps.application.services.orders import (
    CreateOrderUseCase,
    GetOrderUseCase,
    ListOrdersUseCase,
    UpdateOrderStatusUseCase,
    ConfirmOrderUseCase,
    CancelOrderUseCase,
)
from ddd_project.apps.application.services.customers import (
    CreateCustomerUseCase,
    GetCustomerUseCase,
    ListCustomersUseCase,
)


class Container:
    """Simple dependency injection container."""
    
    @staticmethod
    @lru_cache(maxsize=1)
    def get_order_repository() -> OrderRepository:
        return DjangoOrderRepository()

    @staticmethod
    @lru_cache(maxsize=1)
    def get_customer_repository() -> CustomerRepository:
        return DjangoCustomerRepository()


def get_create_order_use_case() -> CreateOrderUseCase:
    return CreateOrderUseCase(Container.get_order_repository())

def get_get_order_use_case() -> GetOrderUseCase:
    return GetOrderUseCase(Container.get_order_repository())

def get_list_orders_use_case() -> ListOrdersUseCase:
    return ListOrdersUseCase(Container.get_order_repository())

def get_update_order_status_use_case() -> UpdateOrderStatusUseCase:
    return UpdateOrderStatusUseCase(Container.get_order_repository())

def get_confirm_order_use_case() -> ConfirmOrderUseCase:
    return ConfirmOrderUseCase(Container.get_order_repository())

def get_cancel_order_use_case() -> CancelOrderUseCase:
    return CancelOrderUseCase(Container.get_order_repository())

def get_create_customer_use_case() -> CreateCustomerUseCase:
    return CreateCustomerUseCase(Container.get_customer_repository())

def get_get_customer_use_case() -> GetCustomerUseCase:
    return GetCustomerUseCase(Container.get_customer_repository())

def get_list_customers_use_case() -> ListCustomersUseCase:
    return ListCustomersUseCase(Container.get_customer_repository())