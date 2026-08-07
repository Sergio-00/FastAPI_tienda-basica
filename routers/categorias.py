from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import seguridad

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


# GET  /categorias/{categoria_id}   -> obtener una (404 si no existe)
@router.get("/{categoria_id}")
def obtener_categoria(categoria_id: int):
    for categoria in categorias:
        if categoria["id"] == categoria_id:
            return categoria
    raise HTTPException(status_code=404, detail="Categoría no encontrada")


# POST /categorias               -> crear (status 201)
@router.post("", status_code=201)
def crear_categoria(
    datos: CategoriaEntrada, usuario: dict = Depends(seguridad.obtener_usuario_actual)
):
    nuevo_id = max((c["id"] for c in categorias), default=0) + 1
    nueva_categoria = {"id": nuevo_id, "nombre": datos.nombre}
    categorias.append(nueva_categoria)
    return {
        "mensaje": "Categoria creada",
        "categoria": nueva_categoria,
        "creado_por": usuario["username"],
    }


# PUT  /categorias/{categoria_id}   -> actualizar el nombre (404 si no existe)
@router.put("/{categoria_id}")
def actualizar_categoria(
    categoria_id: int,
    datos: CategoriaEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    for categoria in categorias:
        if categoria["id"] == categoria_id:
            categoria["nombre"] = datos.nombre
            return {
                "mensaje": "Categoria actualizada",
                "categoria": categoria,
                "modificado_por": usuario["username"],
            }
    raise HTTPException(status_code=404, detail="Categoria no encontrada")


# DELETE /categorias/{categoria_id} -> eliminar (404 si no existe)
@router.delete("/{categoria_id}")
def eliminar_categoria(
    categoria_id: int, admin: dict = Depends(seguridad.requerir_admin)
):
    for categoria in categorias:
        if categoria["id"] == categoria_id:
            categorias.remove(categoria)
            return {
                "mensaje": "Categoria eliminada",
                "categoria": categoria,
                "eliminado_por": admin["username"],
            }
    raise HTTPException(status_code=404, detail="Categoria no encontrada")
