from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/categorias", tags=["Categorias"])


class CategoriaEntrada(BaseModel):
    nombre: str


categorias = [
    {"id": 1, "nombre": "Perifericos"},
    {"id": 2, "nombre": "Pantallas"},
    {"id": 3, "nombre": "Audio"},
]


# LISTAR (resuelto como ejemplo)
@router.get("")
def listar_categorias():
    return categorias


# TODO 1: GET  /categorias/{categoria_id}   -> obtener una (404 si no existe)
# TODO 2: POST /categorias               -> crear (status 201)
# TODO 3: PUT  /categorias/{categoria_id}   -> actualizar el nombre (404 si no existe)
# TODO 4: DELETE /categorias/{categoria_id} -> eliminar (404 si no existe)
