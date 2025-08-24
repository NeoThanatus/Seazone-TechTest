"""
Funções de acesso e manipulação de dados das reservas.
Implementa operações CRUD e consultas relacionadas à entidade Reservations.
"""
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas


async def create_reservation(
        db: AsyncSession,
        reservation: schemas.ReservationCreate,
        total_value: float):
    """
    Cria uma nova reserva no banco de dados.
    Args:
        db: Sessão assíncrona do banco de dados.
        reservation: Dados da reserva a ser criada.
        total_value: Valor total da reserva.
    Returns:
        Instância da reserva criada.
    """

    db_reservation = models.Reservations(
        client_name=reservation.client_name,
        client_email=reservation.client_email,
        start_date=reservation.start_date,
        end_date=reservation.end_date,
        guests_quantity=reservation.guests_quantity,
        property_id=reservation.property_id,
        total_value=total_value
    )

    db.add(db_reservation)
    await db.commit()
    await db.refresh(db_reservation)
    return db_reservation


async def get_reservations(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10):
    """
    Retorna uma lista de reservas com paginação.
    Args:
        db: Sessão assíncrona do banco de dados.
        skip: Número de registros a pular.
        limit: Número máximo de registros a retornar.
    Returns:
        Lista de reservas.
    """
    result = await db.execute(
        select(models.Reservations).offset(skip).limit(limit))
    return result.scalars().all()


async def get_reservation_by_id(
        db: AsyncSession,
        reservation_id: int):
    """
    Busca uma reserva pelo ID.
    Args:
        db: Sessão assíncrona do banco de dados.
        reservation_id: ID da reserva.
    Returns:
        Instância da reserva ou None.
    """
    result = await db.execute(
        select(models.Reservations).filter(
            models.Reservations.reservation_id == reservation_id)
    )
    return result.scalars().first()


async def get_reservation_by_email(
        db: AsyncSession,
        email: str):
    """
    Busca reservas pelo e-mail do cliente.
    Args:
        db: Sessão assíncrona do banco de dados.
        email: E-mail do cliente.
    Returns:
        Lista de reservas.
    """
    result = await db.execute(
        select(models.Reservations).filter(
            models.Reservations.client_email == email)
    )
    return result.scalars().all()


async def get_reservation_by_property(
        db: AsyncSession,
        property_id: int):
    """
    Busca reservas por ID da propriedade.
    Args:
        db: Sessão assíncrona do banco de dados.
        property_id: ID da propriedade.
    Returns:
        Lista de reservas.
    """
    result = await db.execute(
        select(models.Reservations).filter(
            models.Reservations.property_id == property_id
        )
    )
    return result.scalars().all()


async def check_overlap(
        db: AsyncSession,
        property_id: int,
        start_date: date,
        end_date: date):
    """
    Verifica se há sobreposição de datas para uma propriedade.
    Args:
        db: Sessão assíncrona do banco de dados.
        property_id: ID da propriedade.
        start_date: Data inicial.
        end_date: Data final.
    Returns:
        Reserva sobreposta ou None.
    """
    result = await db.execute(
        select(models.Reservations).filter(
            models.Reservations.property_id == property_id,
            models.Reservations.end_date >= start_date,
            models.Reservations.start_date <= end_date
        )
    )
    return result.scalars().first()


async def update_reservation(
        db: AsyncSession,
        reservation_id: int,
        reservation_update: schemas.ReservationUpdate):
    """
    Atualiza os dados de uma reserva existente.
    Args:
        db: Sessão assíncrona do banco de dados.
        reservation_id: ID da reserva.
        reservation_update: Dados para atualização.
    Returns:
        Instância da reserva atualizada ou None.
    """
    db_reservation = await get_reservation_by_id(db, reservation_id)
    if not db_reservation:
        return None

    for key, value in reservation_update.dict(exclude_unset=True).items():
        setattr(db_reservation, key, value)

    await db.commit()
    await db.refresh(db_reservation)
    return db_reservation


async def delete_reservation(
        db: AsyncSession,
        reservation_id: int):
    """
    Remove uma reserva do banco de dados.
    Args:
        db: Sessão assíncrona do banco de dados.
        reservation_id: ID da reserva.
    Returns:
        Instância removida ou None.
    """
    db_reservation = await get_reservation_by_id(db, reservation_id)
    if not db_reservation:
        return None

    await db.delete(db_reservation)
    await db.commit()
    return db_reservation
