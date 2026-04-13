"""API Router - Django Ninja API endpoints"""
from uuid import UUID
from ninja import NinjaAPI
from ninja.errors import HttpError

from ddd_project.apps.application.dtos import (
    OrderCreateDTO,
    OrderResponseDTO,
    OrderUpdateStatusDTO,
    CustomerCreateDTO,
    CustomerResponseDTO,
)
from ddd_project.core.di import (
    get_create_order_use_case,
    get_get_order_use_case,
    get_list_orders_use_case,
    get_update_order_status_use_case,
    get_confirm_order_use_case,
    get_cancel_order_use_case,
    get_create_customer_use_case,
    get_get_customer_use_case,
    get_list_customers_use_case,
)

api = NinjaAPI(title="DDD Order Management API", version="1.0")


@api.post("/orders", response=OrderResponseDTO, tags=["orders"])
def create_order(request, dto: OrderCreateDTO):
    """Create a new order."""
    use_case = get_create_order_use_case()
    return use_case.execute(dto)


@api.get("/orders/{order_id}", response=OrderResponseDTO, tags=["orders"])
def get_order(request, order_id: UUID):
    """Get order by ID."""
    use_case = get_get_order_use_case()
    order = use_case.execute(order_id)
    if order is None:
        raise HttpError(404, "Order not found")
    return order


@api.get("/orders", response=list[OrderResponseDTO], tags=["orders"])
def list_orders(request):
    """List all orders."""
    use_case = get_list_orders_use_case()
    return use_case.execute()


@api.patch("/orders/{order_id}/status", response=OrderResponseDTO, tags=["orders"])
def update_order_status(request, order_id: UUID, dto: OrderUpdateStatusDTO):
    """Update order status."""
    use_case = get_update_order_status_use_case()
    order = use_case.execute(order_id, dto)
    if order is None:
        raise HttpError(404, "Order not found")
    return order


@api.post("/orders/{order_id}/confirm", response=OrderResponseDTO, tags=["orders"])
def confirm_order(request, order_id: UUID):
    """Confirm an order."""
    use_case = get_confirm_order_use_case()
    order = use_case.execute(order_id)
    if order is None:
        raise HttpError(404, "Order not found")
    return order


@api.post("/orders/{order_id}/cancel", response=OrderResponseDTO, tags=["orders"])
def cancel_order(request, order_id: UUID):
    """Cancel an order."""
    use_case = get_cancel_order_use_case()
    order = use_case.execute(order_id)
    if order is None:
        raise HttpError(404, "Order not found")
    return order


@api.post("/customers", response=CustomerResponseDTO, tags=["customers"])
def create_customer(request, dto: CustomerCreateDTO):
    """Create a new customer."""
    use_case = get_create_customer_use_case()
    return use_case.execute(dto)


@api.get("/customers/{customer_id}", response=CustomerResponseDTO, tags=["customers"])
def get_customer(request, customer_id: UUID):
    """Get customer by ID."""
    use_case = get_get_customer_use_case()
    customer = use_case.execute(customer_id)
    if customer is None:
        raise HttpError(404, "Customer not found")
    return customer


@api.get("/customers", response=list[CustomerResponseDTO], tags=["customers"])
def list_customers(request):
    """List all customers."""
    use_case = get_list_customers_use_case()
    return use_case.execute()