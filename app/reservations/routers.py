from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db
from . import schemas, service

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post("/", response_model=schemas.ReservationResponse)
async def create_reservation(reservation_in: schemas.ReservationCreate,
                             db: AsyncSession = Depends(get_db)):
    """
    Endpoint para criar uma nova reserva.
    Args:
        reservation_in: Dados da reserva.
        db: Sessão do banco de dados.
    Returns:
        Reserva criada.
    """
    return await service.create_reservation_service(db, reservation_in)


@router.get("/", response_model=list[schemas.ReservationResponse])
async def list_reservations(client_email: str | None = None,
                            property_id: int | None = None,
                            db: AsyncSession = Depends(get_db)):
    """
    Endpoint para listar reservas com filtros por e-mail ou propriedade.
    Args:
        client_email: E-mail do cliente (opcional).
        property_id: ID da propriedade (opcional).
        db: Sessão do banco de dados.
    Returns:
        Lista de reservas.
    """
    return await service.list_reservations_service(db, client_email,
                                                   property_id)


@router.get("/{reservation_id}", response_model=schemas.ReservationResponse)
async def get_reservation(reservation_id: int,
                          db: AsyncSession = Depends(get_db)):
    """
    Endpoint para buscar uma reserva pelo ID.
    Args:
        reservation_id: ID da reserva.
        db: Sessão do banco de dados.
    Returns:
        Reserva encontrada.
    """
    return await service.get_reservation_service(db, reservation_id)


@router.delete("/{reservation_id}")
async def cancel_reservation(reservation_id: int,
                             db: AsyncSession = Depends(get_db)):
    """
    Endpoint para cancelar (remover) uma reserva.
    Args:
        reservation_id: ID da reserva.
        db: Sessão do banco de dados.
    Returns:
        Status de cancelamento.
    """
    return await service.cancel_reservation_service(db, reservation_id)
