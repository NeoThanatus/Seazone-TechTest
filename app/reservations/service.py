"""
Serviços e regras de negócio para reservas.
Orquestra operações entre repositórios e schemas, aplicando validações e lógica de negócio.
"""
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import repository, schemas
from ..properties import repository as properties_repo


async def create_reservation_service(db: AsyncSession,
                                     reservation_in: schemas.ReservationCreate
                                     ):
    """
    Serviço para criar uma nova reserva.
    Args:
        db: Sessão assíncrona do banco de dados.
        reservation_in: Dados da reserva a ser criada.
    Returns:
        Dados da reserva criada ou exceção HTTP.
    """
    property_ = await properties_repo.get_property_by_id(
        db,
        reservation_in.property_id)
    if not property_:
        raise HTTPException(status_code=404, detail="Property not found")

    if reservation_in.guests_quantity > property_.capacity:
        raise HTTPException(status_code=400, detail="Guests exceed capacity")

    if reservation_in.end_date <= reservation_in.start_date:
        raise HTTPException(status_code=400,
                            detail="End date must be after start date")

    overlap = await repository.check_overlap(db,
                                             reservation_in.property_id,
                                             reservation_in.start_date,
                                             reservation_in.end_date)
    if overlap:
        raise HTTPException(status_code=400,
                            detail="Property not available for these dates")

    nights = (reservation_in.end_date - reservation_in.start_date).days
    total_price = float(property_.price_per_night) * nights

    new_reservation = await repository.create_reservation(
        db,
        reservation_in,
        total_value=total_price)

    return {
        "reservation_id": new_reservation.reservation_id,
        "property_id": new_reservation.property_id,
        "client_name": new_reservation.client_name,
        "client_email": new_reservation.client_email,
        "start_date": new_reservation.start_date,
        "end_date": new_reservation.end_date,
        "guests_quantity": new_reservation.guests_quantity,
        "total_value": new_reservation.total_value,
    }


async def list_reservations_service(db: AsyncSession,
                                    client_email: str | None = None,
                                    property_id: int | None = None):
    """
    Serviço para listar reservas filtrando por e-mail ou propriedade.
    Args:
        db: Sessão assíncrona do banco de dados.
        client_email: E-mail do cliente (opcional).
        property_id: ID da propriedade (opcional).
    Returns:
        Lista de reservas.
    """
    if client_email:
        return await repository.get_reservation_by_email(db, client_email)
    if property_id:
        return await repository.get_reservation_by_property(db, property_id)
    return await repository.get_reservations(db)


async def get_reservation_service(db: AsyncSession, reservation_id: int):
    """
    Serviço para buscar uma reserva pelo ID.
    Args:
        db: Sessão assíncrona do banco de dados.
        reservation_id: ID da reserva.
    Returns:
        Instância da reserva ou exceção 404.
    """
    res = await repository.get_reservation_by_id(db, reservation_id)
    if not res:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return res


async def cancel_reservation_service(db: AsyncSession, reservation_id: int):
    """
    Serviço para cancelar (remover) uma reserva.
    Args:
        db: Sessão assíncrona do banco de dados.
        reservation_id: ID da reserva.
    Returns:
        Status de cancelamento ou exceção 404.
    """
    deleted = await repository.delete_reservation(db, reservation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {"status": "cancelled"}
