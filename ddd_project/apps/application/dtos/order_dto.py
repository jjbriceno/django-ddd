"""Order DTOs - Data Transfer Objects for Orders"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class OrderItemDTO(BaseModel):
    """DTO for order items in requests.
    
    DTO Principles:
    - Flat structure for API requests
    - No domain logic, just data
    """
    product_name: str = Field(..., min_length=1)
    unit_price: float = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class OrderItemResponseDTO(BaseModel):
    """DTO for order items in responses."""
    id: UUID
    product_name: str
    unit_price: float
    quantity: int
    total_price: float

    class Config:
        from_attributes = True


class OrderCreateDTO(BaseModel):
    """DTO for creating orders.
    
    DTO Principles:
    - Validates incoming API data
    - Converts to domain when mapping
    """
    customer_id: Optional[UUID] = None
    items: list[OrderItemDTO] = Field(..., min_length=1)
    shipping_address: str = Field(..., min_length=1)
    notes: str = ""


class OrderUpdateStatusDTO(BaseModel):
    """DTO for updating order status."""
    status: str = Field(..., pattern="^(PENDING|CONFIRMED|PROCESSING|SHIPPED|DELIVERED|CANCELLED)$")


class OrderResponseDTO(BaseModel):
    """DTO for order responses.
    
    DTO Principles:
    - Represents how orders appear in API responses
    - May include computed fields
    """
    id: UUID
    customer_id: Optional[UUID]
    status: str
    items: list[OrderItemResponseDTO]
    total_amount: float
    item_count: int
    shipping_address: str
    notes: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True