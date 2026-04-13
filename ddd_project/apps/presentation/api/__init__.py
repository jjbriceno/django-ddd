"""API Router - Django Ninja API endpoints"""
from uuid import UUID
from ninja import NinjaAPI

from ddd_project.apps.application.dtos import (
    OrderCreateDTO,
    OrderResponseDTO,
    OrderUpdateStatusDTO,
    CustomerCreateDTO,
    CustomerResponseDTO,
)
from ddd_project.core.di import get_order_service, get_customer_service
from ddd_project.apps.presentation.handlers import register_exception_handlers

api = NinjaAPI(title="DDD Order Management API", version="1.0")
register_exception_handlers(api)


@api.post("/orders", response=OrderResponseDTO, tags=["orders"])
def create_order(dto: OrderCreateDTO):
    """Create a new order."""
    service = get_order_service()
    return service.create_order(dto)


@api.get("/orders/{order_id}", response=OrderResponseDTO, tags=["orders"])
def get_order(order_id: UUID):
    """Get order by ID."""
    service = get_order_service()
    order = service.get_order(order_id)
    if order is None:
        return 404, {"error": "Order not found"}
    return order


@api.get("/orders", response=list[OrderResponseDTO], tags=["orders"])
def list_orders():
    """List all orders."""
    service = get_order_service()
    return service.list_orders()


@api.patch("/orders/{order_id}/status", response=OrderResponseDTO, tags=["orders"])
def update_order_status(order_id: UUID, dto: OrderUpdateStatusDTO):
    """Update order status."""
    service = get_order_service()
    order = service.update_status(order_id, dto)
    if order is None:
        return 404, {"error": "Order not found"}
    return order


@api.post("/orders/{order_id}/confirm", response=OrderResponseDTO, tags=["orders"])
def confirm_order(order_id: UUID):
    """Confirm an order."""
    service = get_order_service()
    order = service.confirm_order(order_id)
    if order is None:
        return 404, {"error": "Order not found"}
    return order


@api.post("/orders/{order_id}/cancel", response=OrderResponseDTO, tags=["orders"])
def cancel_order(order_id: UUID):
    """Cancel an order."""
    service = get_order_service()
    order = service.cancel_order(order_id)
    if order is None:
        return 404, {"error": "Order not found"}
    return order


@api.post("/customers", response=CustomerResponseDTO, tags=["customers"])
def create_customer(dto: CustomerCreateDTO):
    """Create a new customer."""
    service = get_customer_service()
    return service.create_customer(dto)


@api.get("/customers/{customer_id}", response=CustomerResponseDTO, tags=["customers"])
def get_customer(customer_id: UUID):
    """Get customer by ID."""
    service = get_customer_service()
    customer = service.get_customer(customer_id)
    if customer is None:
        return 404, {"error": "Customer not found"}
    return customer


@api.get("/customers", response=list[CustomerResponseDTO], tags=["customers"])
def list_customers():
    """List all customers."""
    service = get_customer_service()
    return service.list_customers()