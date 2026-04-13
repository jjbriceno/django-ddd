"""Tests for OrderStatus value object.

Domain Layer Testing Principles:
- Pure unit tests with no external dependencies
- Test status creation and state transitions
- Test valid and invalid transitions
"""
import pytest

from ddd_project.apps.domain.value_objects import OrderStatus, OrderStatusEnum
from ddd_project.apps.domain.exceptions import InvalidOrderStatusError


class TestOrderStatusCreation:
    """Tests for OrderStatus creation."""
    
    def test_create_pending(self):
        status = OrderStatus.pending()
        assert status.value == OrderStatusEnum.PENDING
    
    def test_create_confirmed(self):
        status = OrderStatus.confirmed()
        assert status.value == OrderStatusEnum.CONFIRMED
    
    def test_create_processing(self):
        status = OrderStatus.processing()
        assert status.value == OrderStatusEnum.PROCESSING
    
    def test_create_shipped(self):
        status = OrderStatus.shipped()
        assert status.value == OrderStatusEnum.SHIPPED
    
    def test_create_delivered(self):
        status = OrderStatus.delivered()
        assert status.value == OrderStatusEnum.DELIVERED
    
    def test_create_cancelled(self):
        status = OrderStatus.cancelled()
        assert status.value == OrderStatusEnum.CANCELLED
    
    def test_from_string_valid(self):
        status = OrderStatus.from_string("CONFIRMED")
        assert status.value == OrderStatusEnum.CONFIRMED
    
    def test_from_string_must_be_uppercase(self):
        """Note: from_string requires uppercase input"""
        with pytest.raises(InvalidOrderStatusError):
            OrderStatus.from_string("confirmed")
    
    def test_from_string_invalid_raises_error(self):
        with pytest.raises(InvalidOrderStatusError):
            OrderStatus.from_string("INVALID")
    
    def test_invalid_type_raises_error(self):
        with pytest.raises(InvalidOrderStatusError):
            OrderStatus("INVALID")


class TestOrderStatusTransitions:
    """Tests for valid order status transitions."""
    
    def test_pending_can_confirm(self):
        pending = OrderStatus.pending()
        confirmed = OrderStatus.confirmed()
        assert pending.can_transition_to(confirmed)
    
    def test_pending_can_cancel(self):
        pending = OrderStatus.pending()
        cancelled = OrderStatus.cancelled()
        assert pending.can_transition_to(cancelled)
    
    def test_pending_cannot_ship(self):
        pending = OrderStatus.pending()
        shipped = OrderStatus.shipped()
        assert not pending.can_transition_to(shipped)
    
    def test_confirmed_can_process(self):
        confirmed = OrderStatus.confirmed()
        processing = OrderStatus.processing()
        assert confirmed.can_transition_to(processing)
    
    def test_confirmed_can_cancel(self):
        confirmed = OrderStatus.confirmed()
        cancelled = OrderStatus.cancelled()
        assert confirmed.can_transition_to(cancelled)
    
    def test_processing_can_ship(self):
        processing = OrderStatus.processing()
        shipped = OrderStatus.shipped()
        assert processing.can_transition_to(shipped)
    
    def test_processing_can_cancel(self):
        processing = OrderStatus.processing()
        cancelled = OrderStatus.cancelled()
        assert processing.can_transition_to(cancelled)
    
    def test_shipped_can_deliver(self):
        shipped = OrderStatus.shipped()
        delivered = OrderStatus.delivered()
        assert shipped.can_transition_to(delivered)
    
    def test_shipped_can_cancel(self):
        shipped = OrderStatus.shipped()
        cancelled = OrderStatus.cancelled()
        assert shipped.can_transition_to(cancelled)
    
    def test_delivered_cannot_transition(self):
        delivered = OrderStatus.delivered()
        for status in [
            OrderStatus.pending(),
            OrderStatus.confirmed(),
            OrderStatus.processing(),
            OrderStatus.shipped(),
            OrderStatus.cancelled(),
        ]:
            assert not delivered.can_transition_to(status)
    
    def test_cancelled_cannot_transition(self):
        cancelled = OrderStatus.cancelled()
        for status in [
            OrderStatus.pending(),
            OrderStatus.confirmed(),
            OrderStatus.processing(),
            OrderStatus.shipped(),
            OrderStatus.delivered(),
        ]:
            assert not cancelled.can_transition_to(status)


class TestOrderStatusEquality:
    """Tests for OrderStatus equality."""
    
    def test_same_statuses_are_equal(self):
        s1 = OrderStatus.pending()
        s2 = OrderStatus.pending()
        assert s1 == s2
    
    def test_different_statuses_not_equal(self):
        s1 = OrderStatus.pending()
        s2 = OrderStatus.confirmed()
        assert s1 != s2
    
    def test_hash_consistency(self):
        s1 = OrderStatus.pending()
        s2 = OrderStatus.pending()
        assert hash(s1) == hash(s2)
    
    def test_str_representation(self):
        pending = OrderStatus.pending()
        assert str(pending) == "PENDING"
    
    def test_repr_format(self):
        pending = OrderStatus.pending()
        assert repr(pending) == "OrderStatus(PENDING)"


class TestOrderStatusImmutability:
    """Tests to verify OrderStatus is immutable."""
    
    def test_cannot_modify_value(self, order_status):
        pending = OrderStatus.pending()
        with pytest.raises(AttributeError):
            pending.value = OrderStatusEnum.CONFIRMED
