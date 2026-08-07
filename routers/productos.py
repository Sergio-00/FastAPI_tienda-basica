from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import seguridad

# El router agrupa los endpoints de productos.
router = APIRouter(prefix="/productos", tags=["Productos"])


# Modelo de entrada (sin id: lo asigna el servidor)
class ProductoEntrada(BaseModel):
    nombre: str
    precio: float
    categoria: str


# "Base de datos" en memoria
productos = [
    {
        "id": 1,
        "nombre": "Teclado mecanico",
        "precio": 120000,
        "categoria": "Perifericos",
    },
    {"id": 2, "nombre": "Mouse gamer", "precio": 85000, "categoria": "Perifericos"},
    {"id": 3, "nombre": "Monitor 24", "precio": 650000, "categoria": "Pantallas"},
]


# GET - listar todos publico        GET /productos
@router.get("")
def listar_productos():
    return productos


# GET - obtener uno publico         GET /productos/{producto_id}
@router.get("/{producto_id}")
def obtener_producto(producto_id: int):
    for producto in productos:
        if producto["id"] == producto_id:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")


# POST - crear autenticado             POST /productos
@router.post("", status_code=201)
def crear_producto(
    datos: ProductoEntrada, usuario: dict = Depends(seguridad.obtener_usuario_actual)
):
    nuevo_id = (
        max((p["id"] for p in productos), default=0) + 1
    )  # Alternativa: len(productos) + 1
    nuevo_producto = {
        "id": nuevo_id,
        "nombre": datos.nombre,
        "precio": datos.precio,
        "categoria": datos.categoria,
    }
    productos.append(nuevo_producto)
    return {
        "mensaje": "Producto creado",
        "producto": nuevo_producto,
        "creado_por": usuario["username"],
    }


# UPDATE - actualizar autenticado        PUT /productos/{producto_id}
@router.put("/{producto_id}")
def actualizar_producto(
    producto_id: int,
    datos: ProductoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    for producto in productos:
        if producto["id"] == producto_id:
            producto["nombre"] = datos.nombre
            producto["precio"] = datos.precio
            producto["categoria"] = datos.categoria
            return {
                "mensaje": "Producto actualizado",
                "producto": producto,
                "modificado_por": usuario["username"],
            }
    raise HTTPException(status_code=404, detail="Producto no encontrado")


# DELETE - eliminar autenticado          DELETE /productos/{producto_id}
@router.delete("/{producto_id}")
def eliminar_producto(
    producto_id: int, admin: dict = Depends(seguridad.requerir_admin)
):
    for producto in productos:
        if producto["id"] == producto_id:
            productos.remove(producto)
            return {
                "mensaje": "Producto eliminado",
                "producto": producto,
                "eliminado_por": admin["username"],
            }
    raise HTTPException(status_code=404, detail="Producto no encontrado")
