"""Value Object Exceptions"""


class ValueObjectError(Exception):
    """Base exception for Value Object errors."""
    pass


class InvalidMoneyError(ValueObjectError):
    """Raised when Money value is invalid."""
    def __init__(self, message="Invalid money value"):
        super().__init__(message)


class NegativeMoneyError(InvalidMoneyError):
    """Raised when attempting to create money with negative amount."""
    def __init__(self, amount):
        self.amount = amount
        super().__init__(f"Money amount cannot be negative: {amount}")


class InvalidCurrencyError(ValueObjectError):
    """Raised when currency is not supported."""
    def __init__(self, currency):
        self.currency = currency
        super().__init__(f"Unsupported currency: {currency}")


class MoneyOperationError(ValueObjectError):
    """Raised when money operation fails (different currencies)."""
    def __init__(self, operation):
        super().__init__(f"Cannot {operation} money with different currencies")


class InvalidQuantityError(ValueObjectError):
    """Raised when attempting to create invalid quantity."""
    def __init__(self, value):
        self.value = value
        super().__init__(f"Invalid quantity: {value}")


class NegativeQuantityError(InvalidQuantityError):
    """Raised when attempting to create negative quantity."""
    def __init__(self, value):
        super().__init__(f"Quantity cannot be negative: {value}")


class InvalidAddressError(ValueObjectError):
    """Raised when address is invalid."""
    def __init__(self, message="Invalid address"):
        super().__init__(message)


class InvalidOrderStatusError(ValueObjectError):
    """Raised when order status is invalid."""
    def __init__(self, status):
        self.status = status
        super().__init__(f"Invalid order status: {status}")