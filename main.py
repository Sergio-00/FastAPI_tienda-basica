from fastapi import FastAPI
from routers import productos, categorias, usuarios, administradores, auth

app = FastAPI(
    title="API de la Tienda",
    description="CRUD de productos y categorías organizadas en varios archivos",
    version="2.0.0",
)


# Conectamos los routers de cada recurso
app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(categorias.router)
app.include_router(usuarios.router)
app.include_router(administradores.router)


@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "API de la Tienda funcionando. Visita /docs"}
