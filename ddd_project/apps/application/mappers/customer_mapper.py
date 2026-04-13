"""Customer Mapper - Converts between domain entity and DTOs"""
from typing import Optional

from ddd_project.apps.domain.entities import Customer
from ddd_project.apps.domain.value_objects import Address
from ddd_project.apps.application.dtos import (
    CustomerCreateDTO,
    CustomerResponseDTO,
    AddressDTO,
)


class CustomerMapper:
    """Maps between Customer domain entity and DTOs."""

    @staticmethod
    def to_domain(dto: CustomerCreateDTO) -> Customer:
        """Convert CreateDTO to Customer domain entity."""
        address: Optional[Address] = None
        if dto.address:
            address = Address.create(
                street=dto.address.street,
                city=dto.address.city,
                state=dto.address.state,
                postal_code=dto.address.postal_code,
                country=dto.address.country,
            )

        return Customer(
            name=dto.name,
            email=dto.email,
            address=address,
        )

    @staticmethod
    def to_dto(customer: Customer) -> CustomerResponseDTO:
        """Convert Customer domain entity to ResponseDTO."""
        address_dto: Optional[AddressDTO] = None
        if customer.address:
            address_dto = AddressDTO(
                street=customer.address.street,
                city=customer.address.city,
                state=customer.address.state,
                postal_code=customer.address.postal_code,
                country=customer.address.country,
            )

        return CustomerResponseDTO(
            id=customer.id,
            name=customer.name,
            email=customer.email,
            address=address_dto,
            is_active=customer.is_active,
            created_at=customer.created_at,
            updated_at=customer.updated_at,
        )

    @staticmethod
    def to_dto_list(customers: list[Customer]) -> list[CustomerResponseDTO]:
        """Convert list of customers to list of DTOs."""
        return [CustomerMapper.to_dto(customer) for customer in customers]