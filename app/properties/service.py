"""
Serviços e regras de negócio para propriedades.
Orquestra operações entre repositórios e schemas, aplicando validações e lógica de negócio.
"""
from fastapi import HTTPException
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from . import repository, schemas


async def create_property_service(
    db: AsyncSession, 
    property_in: schemas.PropertyCreate
):
    """
    Serviço para criar uma nova propriedade.
    Args:
        db: Sessão assíncrona do banco de dados.
        property_in: Dados da propriedade a ser criada.
    Returns:
        Instância da propriedade criada.
    """
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
    """
    Serviço para listar propriedades filtrando por diversos critérios.
    Args:
        db: Sessão assíncrona do banco de dados.
        skip, limit: Paginação.
        neighborhood, city, state: Filtros de localização.
        max_price: Preço máximo.
        min_capacity: Capacidade mínima.
    Returns:
        Lista de propriedades.
    """
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
    """
    Serviço para listar propriedades disponíveis em um intervalo de datas.
    Args:
        db: Sessão assíncrona do banco de dados.
        start_date: Data inicial.
        end_date: Data final.
    Returns:
        Lista de propriedades disponíveis.
    """
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
    """
    Serviço para buscar uma propriedade pelo ID.
    Args:
        db: Sessão assíncrona do banco de dados.
        property_id: ID da propriedade.
    Returns:
        Instância da propriedade ou exceção 404.
    """
    property_ = await repository.get_property_by_id(db, property_id)
    if not property_:
        raise HTTPException(status_code=404, detail="Property not found")
    return property_


async def update_property_service(db: AsyncSession, property_id: int,
                                  property_update: schemas.PropertyUpdate):
    """
    Serviço para atualizar uma propriedade existente.
    Args:
        db: Sessão assíncrona do banco de dados.
        property_id: ID da propriedade.
        property_update: Dados para atualização.
    Returns:
        Instância atualizada ou exceção 404.
    """
    updated = await repository.update_property(db, property_id,
                                               property_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Property not found")
    return updated


async def delete_property_service(db: AsyncSession, property_id: int):
    """
    Serviço para remover uma propriedade do banco de dados.
    Args:
        db: Sessão assíncrona do banco de dados.
        property_id: ID da propriedade.
    Returns:
        Status de remoção ou exceção 404.
    """
    deleted = await repository.delete_property(db, property_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Property not found")
    return {"status": "deleted"}
