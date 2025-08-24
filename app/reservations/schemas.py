from datetime import date
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class ReservationBase(BaseModel):
    client_name: str = Field(..., max_length=255)
    client_email: str = EmailStr
    start_date: date
    end_date: date
    guest_quantity: int = Field(..., ge=1)
    property_id: int


class ReservationCreate(ReservationBase):
    """Schema usado no POST /reservation"""
    pass


class ReservationResponde(ReservationBase):
    """Schema de retorno de uma reserva"""
    reservation_id: int
    total_value: Optional[float]

    class Config:
        from_attributes = True
