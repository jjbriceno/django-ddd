"""Tests for Address value object.

Domain Layer Testing Principles:
- Pure unit tests with no external dependencies
- Test value object creation and validation
- Test immutability and equality
"""
import pytest

from ddd_project.apps.domain.value_objects import Address
from ddd_project.apps.domain.exceptions import InvalidAddressError


class TestAddressCreation:
    """Tests for Address creation."""
    
    def test_create_valid_address(self, address):
        addr = address()
        assert addr.street == "123 Main St"
        assert addr.city == "New York"
        assert addr.state == "NY"
        assert addr.postal_code == "10001"
        assert addr.country == "USA"
    
    def test_create_with_custom_values(self):
        addr = Address.create(
            street="456 Oak Ave",
            city="Los Angeles",
            state="CA",
            postal_code="90001",
            country="USA",
        )
        assert addr.street == "456 Oak Ave"
        assert addr.city == "Los Angeles"
        assert addr.state == "CA"
        assert addr.postal_code == "90001"
        assert addr.country == "USA"
    
    def test_create_strips_whitespace(self):
        addr = Address.create(
            street="  789 Pine St  ",
            city="  Chicago  ",
            state="  IL  ",
            postal_code="  60601  ",
            country="  USA  ",
        )
        assert addr.street == "789 Pine St"
        assert addr.city == "Chicago"
        assert addr.state == "IL"
        assert addr.postal_code == "60601"
        assert addr.country == "USA"


class TestAddressValidation:
    """Tests for Address validation."""
    
    def test_empty_street_raises_error(self):
        with pytest.raises(InvalidAddressError) as exc_info:
            Address.create("", "Chicago", "IL", "60601", "USA")
        assert "Street" in str(exc_info.value)
    
    def test_empty_city_raises_error(self):
        with pytest.raises(InvalidAddressError) as exc_info:
            Address.create("123 Main", "", "IL", "60601", "USA")
        assert "City" in str(exc_info.value)
    
    def test_empty_country_raises_error(self):
        with pytest.raises(InvalidAddressError) as exc_info:
            Address.create("123 Main", "Chicago", "IL", "60601", "")
        assert "Country" in str(exc_info.value)
    
    def test_state_can_be_empty(self):
        addr = Address.create("123 Main", "Chicago", "", "60601", "USA")
        assert addr.state == ""


class TestAddressEquality:
    """Tests for Address equality and hashing."""
    
    def test_identical_addresses_are_equal(self, address):
        addr1 = address()
        addr2 = address()
        assert addr1 == addr2
    
    def test_different_streets_not_equal(self):
        addr1 = Address.create("123 Main St", "NYC", "", "10001", "USA")
        addr2 = Address.create("456 Main St", "NYC", "", "10001", "USA")
        assert addr1 != addr2
    
    def test_different_cities_not_equal(self):
        addr1 = Address.create("123 Main St", "NYC", "", "10001", "USA")
        addr2 = Address.create("123 Main St", "LA", "", "10001", "USA")
        assert addr1 != addr2
    
    def test_hash_consistency(self, address):
        addr1 = address()
        addr2 = address()
        assert hash(addr1) == hash(addr2)
    
    def test_can_be_used_in_set(self, address):
        addr1 = address()
        addr2 = address()
        s = {addr1, addr2}
        assert len(s) == 1


class TestAddressImmutability:
    """Tests to verify Address is immutable."""
    
    def test_cannot_modify_street_directly(self, address):
        addr = address()
        with pytest.raises(AttributeError):
            addr.street = "456 New St"
    
    def test_cannot_modify_city_directly(self, address):
        addr = address()
        with pytest.raises(AttributeError):
            addr.city = "Los Angeles"
    
    def test_repr_format(self, address):
        addr = address()
        assert repr(addr) == "Address(123 Main St, New York, USA)"
