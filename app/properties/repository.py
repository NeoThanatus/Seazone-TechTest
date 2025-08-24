from datetime import date
from typing import Optional
from ..reservations import models as reservation_models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas


async def create_property(
        db: AsyncSession,
        property_: schemas.PropertyCreate):
    db_property = models.Properties(
        title=property_.title,
        address_street=property_.address_street,
        address_number=property_.address_number,
        address_neighborhood=property_.address_neighborhood,
        address_city=property_.address_city,
        address_state=property_.address_state,
        country=property_.country,
        rooms=property_.rooms,
        capacity=property_.capacity,
        price_per_night=property_.price_per_night,
    )
    db.add(db_property)
    await db.commit()
    await db.refresh(db_property)
    return db_property


async def get_properties(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10):
    result = await db.execute(
        select(models.Properties).offset(skip).limit(limit))
    return result.scalars().all()


async def get_property_by_id(
        db: AsyncSession,
        property_id: int):
    result = await db.execute(
        select(models.Properties).filter(
            models.Properties.property_id == property_id)
    )
    return result.scalars().first()


async def get_available_properties(
    db: AsyncSession,
    start_date: date,
    end_date: date
):
    subquery = (
        select(reservation_models.Reservations.property_id)
        .filter(
            reservation_models.Reservations.start_date < end_date,
            reservation_models.Reservations.end_date > start_date
        )
        .distinct()
    )

    query = (
        select(models.Properties)
        .filter(models.Properties.property_id.notin_(subquery))
    )

    result = await db.execute(query)
    return result.scalars().all()


async def filter_properties(
        db: AsyncSession,
        street: Optional[str] = None,
        neighborhood: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        max_price: Optional[float] = None,
        min_capacity: Optional[int] = None):
    query = select(models.Properties)
    if street:
        query = query.filter(
            models.Properties.address_street.ilike(f"%{street}%"))
    if neighborhood:
        query = query.filter(
            models.Properties.address_neighborhood.ilike(f"%{neighborhood}%"))
    if city:
        query = query.filter(
            models.Properties.address_city.ilike(f"%{city}%"))
    if state:
        query = query.filter(
            models.Properties.address_state.ilike(f"%{state}%"))
    if max_price:
        query = query.filter(
            models.Properties.price_per_night <= max_price)
    if min_capacity:
        query = query.filter(
            models.Properties.capacity >= min_capacity)

    result = await db.execute(query)
    return result.scalars().all()


async def update_property(
        db: AsyncSession,
        property_id: int,
        property_update: schemas.PropertyUpdate):
    db_property = await get_property_by_id(db, property_id)
    if not db_property:
        return None

    for key, value in property_update.dict(exclude_unset=True).items():
        setattr(db_property, key, value)

    await db.commit()
    await db.refresh(db_property)
    return db_property


async def delete_property(
        db: AsyncSession,
        property_id: int):
    db_property = await get_property_by_id(db, property_id)
    if not db_property:
        return None

    await db.delete(db_property)
    await db.commit()
    return db_property
