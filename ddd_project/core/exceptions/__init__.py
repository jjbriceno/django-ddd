"""Core Exceptions - Application-level exceptions"""


class ApplicationException(Exception):
    """Base exception for application errors."""
    pass


class UseCaseError(ApplicationException):
    """Raised when a use case fails."""
    pass


class EntityNotFoundError(ApplicationException):
    """Raised when an entity is not found."""
    def __init__(self, entity_type: str, entity_id):
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} not found: {entity_id}")