from fastapi import HTTPException
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from . import repository, schemas


async def create_property_service(
    db: AsyncSession, 
    property_in: schemas.PropertyCreate
):
    return await repository.create_property(db, property_in)


async def list_properties_service(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    neighborhood: str | None = None,
    city: str | None = None,
    state: str | None = None,
    max_price: float | None = None,
    min_capacity: int | None = None
):
    return await repository.filter_properties(
        db,
        neighborhood=neighborhood,
        city=city,
        state=state,
        max_price=max_price,
        min_capacity=min_capacity,
    )


async def list_available_properties_service(
    db: AsyncSession,
    start_date: date,
    end_date: date
):
    if end_date <= start_date:
        raise HTTPException(
            status_code=400,
            detail="End date must be after start date"
        )

    available_properties = await repository.get_available_properties(
        db,
        start_date=start_date,
        end_date=end_date
    )

    return available_properties


async def get_property_service(db: AsyncSession, property_id: int):
    property_ = await repository.get_property_by_id(db, property_id)
    if not property_:
        raise HTTPException(status_code=404, detail="Property not found")
    return property_


async def update_property_service(db: AsyncSession, property_id: int,
                                  property_update: schemas.PropertyUpdate):
    updated = await repository.update_property(db, property_id,
                                               property_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Property not found")
    return updated


async def delete_property_service(db: AsyncSession, property_id: int):
    deleted = await repository.delete_property(db, property_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Property not found")
    return {"status": "deleted"}
