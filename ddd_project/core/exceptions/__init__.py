"""Core Exceptions - Domain and Application exceptions"""


class DomainException(Exception):
    """Base exception for domain errors."""
    pass


class EntityNotFoundError(DomainException):
    """Raised when an entity is not found."""
    pass


class InvalidStateTransitionError(DomainException):
    """Raised when an invalid state transition is attempted."""
    pass


class ValidationError(DomainException):
    """Raised when validation fails."""
    pass