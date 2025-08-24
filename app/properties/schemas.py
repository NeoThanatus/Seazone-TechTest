from pydantic import BaseModel, Field
from typing import List, Optional


class PropertyBase(BaseModel):
    title: str = Field(..., max_length=255)
    address_street: str = Field(..., max_length=255)
    address_number: str = Field(..., max_length=255)
    address_neighborhood: str = Field(..., max_length=255)
    address_city: str = Field(..., max_length=255)
    address_state: str = Field(..., max_length=255)
    rooms: int
    capacity: int
    price_par_night: float


class PropertyCreate(PropertyBase):
    """Schema usado no POST /properties"""
    pass


class PropertyResponse(PropertyBase):
    """Schema de retorno de uma propriedade"""
    property_id: int
    reservation: Optional[List[int]] = []

    class Config:
        from_attributes = True
