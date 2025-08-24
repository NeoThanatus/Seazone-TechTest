from datetime import date
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class ReservationBase(BaseModel):
    """
    Schema base para reservas.
    Define campos comuns usados em criação, atualização e resposta.
    """
    client_name: str = Field(..., max_length=255)
    client_email: EmailStr
    start_date: date
    end_date: date
    guests_quantity: int = Field(..., ge=1)
    property_id: int


class ReservationCreate(ReservationBase):
    """
    Schema usado no POST /reservation.
    Define campos obrigatórios para criação de uma reserva.
    """
    pass


class ReservationUpdate(BaseModel):
    """
    Schema usado no PUT/PATCH /reservations/{id}.
    Permite atualização parcial dos campos da reserva.
    """
    client_name: Optional[str] = None
    client_email: Optional[EmailStr] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    guests_quantity: Optional[int] = None


class ReservationResponse(ReservationBase):
    """
    Schema de retorno de uma reserva.
    Inclui ID e valor total da reserva.
    """
    reservation_id: int
    total_value: Optional[float] = None

    class Config:
        from_attributes = True
