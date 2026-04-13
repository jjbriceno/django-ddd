"""Customer Domain Exceptions"""


class CustomerDomainError(Exception):
    """Base exception for Customer domain errors."""
    pass


class CustomerNotFoundError(CustomerDomainError):
    """Raised when a customer is not found."""
    def __init__(self, customer_id):
        self.customer_id = customer_id
        super().__init__(f"Customer not found: {customer_id}")


class CustomerAlreadyExistsError(CustomerDomainError):
    """Raised when attempting to create a customer that already exists."""
    def __init__(self, email):
        self.email = email
        super().__init__(f"Customer already exists with email: {email}")


class InvalidCustomerEmailError(CustomerDomainError):
    """Raised when customer email is invalid."""
    def __init__(self, email):
        self.email = email
        super().__init__(f"Invalid customer email: {email}")


class CustomerValidationError(CustomerDomainError):
    """Raised when customer validation fails."""
    pass


class RequiredCustomerNameError(CustomerValidationError):
    """Raised when customer name is required but missing."""
    def __init__(self):
        super().__init__("Customer name is required")


class RequiredCustomerEmailError(CustomerValidationError):
    """Raised when customer email is required but missing."""
    def __init__(self):
        super().__init__("Customer email is required")