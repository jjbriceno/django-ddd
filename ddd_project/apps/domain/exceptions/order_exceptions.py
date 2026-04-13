"""Order Domain Exceptions"""


class OrderDomainError(Exception):
    """Base exception for Order domain errors."""
    pass


class OrderNotFoundError(OrderDomainError):
    """Raised when an order is not found."""
    def __init__(self, order_id):
        self.order_id = order_id
        super().__init__(f"Order not found: {order_id}")


class OrderAlreadyExistsError(OrderDomainError):
    """Raised when attempting to create an order that already exists."""
    def __init__(self, order_id):
        self.order_id = order_id
        super().__init__(f"Order already exists: {order_id}")


class EmptyOrderError(OrderDomainError):
    """Raised when attempting to confirm an order with no items."""
    def __init__(self):
        super().__init__("Cannot confirm order without items")


class InvalidOrderStatusTransitionError(OrderDomainError):
    """Raised when an invalid status transition is attempted."""
    def __init__(self, current_status, target_status):
        self.current_status = current_status
        self.target_status = target_status
        super().__init__(
            f"Invalid status transition from {current_status} to {target_status}"
        )


class CannotModifyOrderError(OrderDomainError):
    """Raised when attempting to modify a non-pending order."""
    def __init__(self, action):
        self.action = action
        super().__init__(f"Cannot {action} order that is not pending")