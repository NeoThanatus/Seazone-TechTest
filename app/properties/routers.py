"""
Rotas da API para operações relacionadas a propriedades.
Define endpoints REST para criação, listagem e consulta de propriedades.
"""
from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db
from . import schemas, service

router = APIRouter(prefix="/properties", tags=["Properties"])


@router.post("/", response_model=schemas.PropertyResponse)
async def create_property(property_in: schemas.PropertyCreate,
                          db: AsyncSession = Depends(get_db)):
    """
    Endpoint para criar uma nova propriedade.
    Args:
        property_in: Dados da propriedade.
        db: Sessão do banco de dados.
    Returns:
        Propriedade criada.
    """
    return await service.create_property_service(db, property_in)


@router.get("/", response_model=list[schemas.PropertyResponse])
async def list_properties(
    skip: int = 0,
    limit: int = 10,
    neighborhood: str | None = None,
    city: str | None = None,
    state: str | None = None,
    max_price: float | None = None,
    min_capacity: int | None = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para listar propriedades com filtros e paginação.
    Args:
        skip, limit: Paginação.
        neighborhood, city, state: Filtros de localização.
        max_price: Preço máximo.
        min_capacity: Capacidade mínima.
        db: Sessão do banco de dados.
    Returns:
        Lista de propriedades.
    """
    return await service.list_properties_service(
        db,
        skip=skip,
        limit=limit,
        neighborhood=neighborhood,
        city=city,
        state=state,
        max_price=max_price,
        min_capacity=min_capacity,
    )


@router.get("/availability")
async def get_property_availability(
    start_date: date,
    end_date: date,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para consultar propriedades disponíveis em um intervalo de datas.
    Args:
        start_date: Data inicial.
        end_date: Data final.
        db: Sessão do banco de dados.
    Returns:
        Lista de propriedades disponíveis.
    """
    return await service.list_available_properties_service(
        db,
        start_date,
        end_date
    )


@router.get("/{property_id}", response_model=schemas.PropertyResponse)
async def get_property(property_id: int, db: AsyncSession = Depends(get_db)):
    """
    Endpoint para buscar uma propriedade pelo ID.
    Args:
        property_id: ID da propriedade.
        db: Sessão do banco de dados.
    Returns:
        Propriedade encontrada.
    """
    return await service.get_property_service(db, property_id)


@router.put("/{property_id}", response_model=schemas.PropertyResponse)
async def update_property(property_id: int,
                          property_update: schemas.PropertyUpdate,
                          db: AsyncSession = Depends(get_property)):
    """
    Endpoint para atualizar uma propriedade existente.
    Args:
        property_id: ID da propriedade.
        property_update: Dados para atualização.
        db: Sessão do banco de dados.
    Returns:
        Propriedade atualizada.
    """
    return await service.update_property_service(db, property_id, get_db)


@router.delete("/{property_id}")
async def delete_property(property_id: int,
                          db: AsyncSession = Depends(get_db)):
    """
    Endpoint para remover uma propriedade do banco de dados.
    Args:
        property_id: ID da propriedade.
        db: Sessão do banco de dados.
    Returns:
        Status de remoção.
    """
    return await service.delete_property_service(db, property_id)
