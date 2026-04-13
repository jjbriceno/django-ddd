"""Customer DTOs - Data Transfer Objects for Customers"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr


class AddressDTO(BaseModel):
    """DTO for address data."""
    street: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    state: str = ""
    postal_code: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)


class CustomerCreateDTO(BaseModel):
    """DTO for creating customers."""
    name: str = Field(..., min_length=1)
    email: EmailStr
    address: Optional[AddressDTO] = None


class CustomerResponseDTO(BaseModel):
    """DTO for customer responses."""
    id: UUID
    name: str
    email: str
    address: Optional[AddressDTO]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True