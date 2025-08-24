from pydantic import BaseModel, Field
from typing import List, Optional


class PropertyBase(BaseModel):
    title: str = Field(..., max_length=255)
    address_street: str = Field(..., max_length=255)
    address_number: str = Field(..., max_length=255)
    address_neighborhood: str = Field(..., max_length=255)
    address_city: str = Field(..., max_length=255)
    address_state: str = Field(..., max_length=255)
    country: str = Field(..., max_length=255)
    rooms: int
    capacity: int
    price_per_night: float


class PropertyCreate(PropertyBase):
    """Schema usado no POST /properties"""
    title: str = Field(..., min_length=1)
    address_street: str = Field(..., min_length=1)
    price_per_night: float = Field(..., ge=0)
    pass


class PropertyUpdate(BaseModel):
    """Schema usado no PUT/PATCH /properties/{id}"""
    title: Optional[str] = None
    address_street: Optional[str] = None
    address_number: Optional[str] = None
    address_neighborhood: Optional[str] = None
    address_city: Optional[str] = None
    address_state: Optional[str] = None
    country: Optional[str] = None
    rooms: Optional[int] = None
    capacity: Optional[int] = None
    price_per_night: Optional[float] = None


class PropertyResponse(PropertyBase):
    """Schema de retorno de uma propriedade"""
    property_id: int
    reservation: Optional[List[int]] = []

    class Config:
        from_attributes = True
