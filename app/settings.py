"""
Configuração de variáveis de ambiente e settings globais da aplicação.
Utiliza Pydantic para carregar dados do arquivo .env.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    DATABASE_KEY: str = ""
    SYNC_DATABASE_URL: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
