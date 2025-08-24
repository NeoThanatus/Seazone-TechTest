from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas


async def create_reservation(
        db: AsyncSession,
        reservation: schemas.ReservationCreate,
        total_value: float):

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
    result = await db.execute(
        select(models.Reservations).offset(skip).limit(limit))
    return result.scalars().all()


async def get_reservation_by_id(
        db: AsyncSession,
        reservation_id: int):
    result = await db.execute(
        select(models.Reservations).filter(
            models.Reservations.reservation_id == reservation_id)
    )
    return result.scalars().first()


async def get_reservation_by_email(
        db: AsyncSession,
        email: str):
    result = await db.execute(
        select(models.Reservations).filter(
            models.Reservations.client_email == email)
    )
    return result.scalars().all()


async def get_reservation_by_property(
        db: AsyncSession,
        property_id: int):
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
    db_reservation = await get_reservation_by_id(db, reservation_id)
    if not db_reservation:
        return None

    await db.delete(db_reservation)
    await db.commit()
    return db_reservation
