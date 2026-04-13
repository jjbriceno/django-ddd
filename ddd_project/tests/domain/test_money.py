"""Tests for Money value object.

Domain Layer Testing Principles:
- Pure unit tests with no external dependencies
- Test value object creation, validation, and operations
- Test immutability and equality
- Test exception raising for invalid states
"""
import pytest
from decimal import Decimal

from ddd_project.apps.domain.value_objects import Money
from ddd_project.apps.domain.exceptions import (
    InvalidCurrencyError,
    NegativeMoneyError,
    MoneyOperationError,
)


class TestMoneyCreation:
    """Tests for Money creation."""
    
    def test_create_with_float(self):
        money = Money.create(10.50, "USD")
        assert money.amount == Decimal("10.50")
        assert money.currency == "USD"
    
    def test_create_with_decimal(self):
        money = Money.create(Decimal("99.99"), "EUR")
        assert money.amount == Decimal("99.99")
        assert money.currency == "EUR"
    
    def test_create_with_integer(self):
        money = Money.create(100, "GBP")
        assert money.amount == Decimal("100")
        assert money.currency == "GBP"
    
    def test_zero_money(self):
        money = Money.zero("USD")
        assert money.amount == Decimal("0")
        assert money.currency == "USD"
    
    def test_zero_money_with_default_currency(self):
        money = Money.zero()
        assert money.amount == Decimal("0")
        assert money.currency == "USD"
    
    def test_invalid_currency_raises_error(self):
        with pytest.raises(InvalidCurrencyError) as exc_info:
            Money.create(10, "INVALID")
        assert exc_info.value.currency == "INVALID"
    
    def test_negative_amount_raises_error(self):
        with pytest.raises(NegativeMoneyError) as exc_info:
            Money.create(-10, "USD")
        assert exc_info.value.amount == Decimal("-10")


class TestMoneyOperations:
    """Tests for Money arithmetic operations."""
    
    def test_add_same_currency(self, money_usd):
        m1 = money_usd(10)
        m2 = money_usd(5)
        result = m1.add(m2)
        assert result.amount == Decimal("15")
        assert result.currency == "USD"
    
    def test_add_different_currencies_raises_error(self, money_usd, money_eur):
        m1 = money_usd(10)
        m2 = money_eur(5)
        with pytest.raises(MoneyOperationError):
            m1.add(m2)
    
    def test_multiply(self, money_usd):
        money = money_usd(10)
        result = money.multiply(3)
        assert result.amount == Decimal("30")
        assert result.currency == "USD"
    
    def test_multiply_with_decimal(self, money_usd):
        money = money_usd(10)
        result = money.multiply(1.5)
        assert result.amount == Decimal("15")
    
    def test_multiply_by_zero(self, money_usd):
        money = money_usd(100)
        result = money.multiply(0)
        assert result.amount == Decimal("0")


class TestMoneyEquality:
    """Tests for Money equality and hashing."""
    
    def test_equal_amounts_same_currency(self):
        m1 = Money.create(10, "USD")
        m2 = Money.create(10, "USD")
        assert m1 == m2
    
    def test_different_amounts_not_equal(self):
        m1 = Money.create(10, "USD")
        m2 = Money.create(20, "USD")
        assert m1 != m2
    
    def test_same_amount_different_currency_not_equal(self):
        m1 = Money.create(10, "USD")
        m2 = Money.create(10, "EUR")
        assert m1 != m2
    
    def test_hash_consistency(self):
        m1 = Money.create(10, "USD")
        m2 = Money.create(10, "USD")
        assert hash(m1) == hash(m2)
    
    def test_can_be_used_in_set(self):
        m1 = Money.create(10, "USD")
        m2 = Money.create(10, "USD")
        s = {m1, m2}
        assert len(s) == 1
    
    def test_can_be_used_as_dict_key(self):
        m1 = Money.create(10, "USD")
        d = {m1: "value"}
        assert d[m1] == "value"


class TestMoneyImmutability:
    """Tests to verify Money is immutable."""
    
    def test_operations_return_new_instance(self, money_usd):
        original = money_usd(10)
        result = original.add(money_usd(5))
        assert original.amount == Decimal("10")
        assert result.amount == Decimal("15")
    
    def test_cannot_modify_amount_directly(self, money_usd):
        money = money_usd(10)
        with pytest.raises(AttributeError):
            money.amount = Decimal("20")
    
    def test_cannot_modify_currency_directly(self, money_usd):
        money = money_usd(10)
        with pytest.raises(AttributeError):
            money.currency = "EUR"
    
    def test_repr_format(self, money_usd):
        money = money_usd(10.50)
        assert "10.5" in repr(money) or "10.50" in repr(money)
        assert "USD" in repr(money)
