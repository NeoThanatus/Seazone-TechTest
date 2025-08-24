from fastapi import FastAPI
"""
Arquivo principal da aplicação FastAPI.
Responsável por inicializar a API, registrar os routers de propriedades e reservas.
"""
from fastapi import FastAPI
from .properties import routers as properties_router
from .reservations import routers as reservations_router

app = FastAPI(title="Seazone API")

app.include_router(properties_router.router)
app.include_router(reservations_router.router)
