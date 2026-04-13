"""Global Exception Handlers"""
from ninja import NinjaAPI
from ninja.errors import HttpError

from ddd_project.core.exceptions import DomainException


def register_exception_handlers(api: NinjaAPI) -> None:
    """Register global exception handlers.
    
    Error Handling Principles:
    - Map domain exceptions to HTTP errors
    - Consistent error response format
    - Separate error handling from business logic
    """
    
    @api.exception_handler(DomainException)
    def handle_domain_exception(request, exc: DomainException):
        return 400, {"error": str(exc)}

    @api.exception_handler(ValueError)
    def handle_value_error(request, exc: ValueError):
        return 400, {"error": str(exc)}

    @api.exception_handler(Exception)
    def handle_generic_exception(request, exc: Exception):
        return 500, {"error": "Internal server error"}