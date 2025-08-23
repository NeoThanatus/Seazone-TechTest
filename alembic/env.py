import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from app.settings import settings
from app.db import Base
from app.properties.models import Properties
from app.reservations.models import Reservations


# Config Alembic
config = context.config
config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadados das tabelas
target_metadata = Base.metadata


# Função offline
def run_migrations_offline() -> None:
    """Executa migrações sem conexão ativa."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# Função de execução síncrona das migrations
def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


# Função online assíncrona
async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


# Função online que Alembic chama
def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


# Execução
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
