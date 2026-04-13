"""Tests for Quantity value object.

Domain Layer Testing Principles:
- Pure unit tests with no external dependencies
- Test value object creation and validation
- Test immutability and operations
"""
import pytest

from ddd_project.apps.domain.value_objects import Quantity
from ddd_project.apps.domain.exceptions import InvalidQuantityError, NegativeQuantityError


class TestQuantityCreation:
    """Tests for Quantity creation."""
    
    def test_create_valid_quantity(self, quantity):
        qty = quantity(5)
        assert qty.value == 5
    
    def test_create_zero_quantity(self, quantity):
        qty = quantity(0)
        assert qty.value == 0
    
    def test_zero_class_method(self):
        qty = Quantity.zero()
        assert qty.value == 0
    
    def test_negative_quantity_raises_error(self):
        with pytest.raises(NegativeQuantityError):
            Quantity.create(-1)
    
    def test_float_quantity_raises_error(self):
        with pytest.raises(InvalidQuantityError):
            Quantity.create(1.5)
    
    def test_string_quantity_raises_error(self):
        with pytest.raises(InvalidQuantityError):
            Quantity.create("1")


class TestQuantityOperations:
    """Tests for Quantity arithmetic operations."""
    
    def test_add(self, quantity):
        q1 = quantity(5)
        q2 = quantity(3)
        result = q1.add(q2)
        assert result.value == 8
    
    def test_subtract(self, quantity):
        q1 = quantity(5)
        q2 = quantity(3)
        result = q1.subtract(q2)
        assert result.value == 2
    
    def test_subtract_resulting_in_negative_raises_error(self, quantity):
        q1 = quantity(3)
        q2 = quantity(5)
        with pytest.raises(NegativeQuantityError):
            q1.subtract(q2)


class TestQuantityEquality:
    """Tests for Quantity equality."""
    
    def test_same_values_are_equal(self, quantity):
        q1 = quantity(5)
        q2 = quantity(5)
        assert q1 == q2
    
    def test_different_values_not_equal(self, quantity):
        q1 = quantity(5)
        q2 = quantity(3)
        assert q1 != q2
    
    def test_hash_consistency(self, quantity):
        q1 = quantity(5)
        q2 = quantity(5)
        assert hash(q1) == hash(q2)


class TestQuantityImmutability:
    """Tests to verify Quantity is immutable."""
    
    def test_operations_return_new_instance(self, quantity):
        original = quantity(5)
        result = original.add(quantity(3))
        assert original.value == 5
        assert result.value == 8
    
    def test_cannot_modify_value_directly(self, quantity):
        qty = quantity(5)
        with pytest.raises(AttributeError):
            qty.value = 10
    
    def test_int_conversion(self, quantity):
        qty = quantity(5)
        assert int(qty) == 5
    
    def test_repr_format(self, quantity):
        qty = quantity(5)
        assert repr(qty) == "Quantity(5)"
