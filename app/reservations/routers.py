from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db
from . import schemas, service

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post("/", response_model=schemas.ReservationResponse)
async def create_reservation(reservation_in: schemas.ReservationCreate,
                             db: AsyncSession = Depends(get_db)):
    return await service.create_reservation_service(db, reservation_in)


@router.get("/", response_model=list[schemas.ReservationResponse])
async def list_reservations(client_email: str | None = None,
                            property_id: int | None = None,
                            db: AsyncSession = Depends(get_db)):
    return await service.list_reservations_service(db, client_email,
                                                   property_id)


@router.get("/{reservation_id}", response_model=schemas.ReservationResponse)
async def get_reservation(reservation_id: int,
                          db: AsyncSession = Depends(get_db)):
    return await service.get_reservation_service(db, reservation_id)


@router.delete("/{reservation_id}")
async def cancel_reservation(reservation_id: int,
                             db: AsyncSession = Depends(get_db)):
    return await service.cancel_reservation_service(db, reservation_id)
