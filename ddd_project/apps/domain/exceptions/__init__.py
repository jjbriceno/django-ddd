"""Domain Exceptions"""
from .order_exceptions import (
    OrderDomainError,
    OrderNotFoundError,
    OrderAlreadyExistsError,
    EmptyOrderError,
    InvalidOrderStatusTransitionError,
    CannotModifyOrderError,
)
from .customer_exceptions import (
    CustomerDomainError,
    CustomerNotFoundError,
    CustomerAlreadyExistsError,
    InvalidCustomerEmailError,
    CustomerValidationError,
    RequiredCustomerNameError,
    RequiredCustomerEmailError,
)
from .value_object_exceptions import (
    ValueObjectError,
    InvalidMoneyError,
    NegativeMoneyError,
    InvalidCurrencyError,
    MoneyOperationError,
    InvalidQuantityError,
    NegativeQuantityError,
    InvalidAddressError,
    InvalidOrderStatusError,
)

__all__ = [
    "OrderDomainError",
    "OrderNotFoundError",
    "OrderAlreadyExistsError",
    "EmptyOrderError",
    "InvalidOrderStatusTransitionError",
    "CannotModifyOrderError",
    "CustomerDomainError",
    "CustomerNotFoundError",
    "CustomerAlreadyExistsError",
    "InvalidCustomerEmailError",
    "CustomerValidationError",
    "RequiredCustomerNameError",
    "RequiredCustomerEmailError",
    "ValueObjectError",
    "InvalidMoneyError",
    "NegativeMoneyError",
    "InvalidCurrencyError",
    "MoneyOperationError",
    "InvalidQuantityError",
    "NegativeQuantityError",
    "InvalidAddressError",
    "InvalidOrderStatusError",
]