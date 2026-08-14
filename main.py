from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import crear_tablas, sembrar_datos
from routers import (
    productos,
    categorias,
    usuarios,
    administradores,
    auth,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()
    sembrar_datos()

    yield


app = FastAPI(
    title="API de la Tienda",
    description="CRUD de productos y categorías con SQLite3",
    version="3.0.0",
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(categorias.router)
app.include_router(usuarios.router)
app.include_router(administradores.router)


@app.get("/", tags=["Inicio"])
def inicio():
    return {
        "mensaje": "API de la Tienda funcionando. Visita http://127.0.0.1:8000/docs"
    }
