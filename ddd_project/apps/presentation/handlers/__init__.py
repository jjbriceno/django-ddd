"""Global Exception Handlers"""
from ninja import NinjaAPI

from ddd_project.apps.domain.exceptions import (
    OrderDomainError,
    CustomerDomainError,
    ValueObjectError,
)
from ddd_project.core.exceptions import ApplicationException


def register_exception_handlers(api: NinjaAPI) -> None:
    """Register global exception handlers."""

    @api.exception_handler(ApplicationException)
    def handle_application_exception(request, exc: ApplicationException):
        return 500, {"error": str(exc)}

    @api.exception_handler(OrderDomainError)
    def handle_order_domain_error(request, exc: OrderDomainError):
        return 400, {"error": str(exc), "type": "order_error"}

    @api.exception_handler(CustomerDomainError)
    def handle_customer_domain_error(request, exc: CustomerDomainError):
        return 400, {"error": str(exc), "type": "customer_error"}

    @api.exception_handler(ValueObjectError)
    def handle_value_object_error(request, exc: ValueObjectError):
        return 400, {"error": str(exc), "type": "validation_error"}

    @api.exception_handler(Exception)
    def handle_generic_exception(request, exc: Exception):
        return 500, {"error": "Internal server error"}