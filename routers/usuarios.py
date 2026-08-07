from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import seguridad

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


class UsuarioEntrada(BaseModel):
    nombre: str
    correo: str
    clave: str


usuarios = [
    {"id": 1, "nombre": "Pepe", "correo": "pepe@correo.com", "clave": "claveSegura123"},
    {
        "id": 2,
        "nombre": "Maria",
        "correo": "maria@correo.com",
        "clave": "clave123Segura",
    },
    {"id": 3, "nombre": "David", "correo": "david@correo.com", "clave": "Segura123"},
]


@router.get("")
def listar_usuarios():
    return usuarios


@router.get("/{usuario_id}")
def obtener_usuario(usuario_id: int):
    for usuario in usuarios:
        if usuario["id"] == usuario_id:
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.post("", status_code=201)
def crear_usuario(
    datos: UsuarioEntrada,
    usuario_actual: dict = Depends(seguridad.obtener_usuario_actual),
):
    nuevo_id = max((u["id"] for u in usuarios), default=0) + 1
    nuevo_usuario = {
        "id": nuevo_id,
        "nombre": datos.nombre,
        "correo": datos.correo,
        "clave": datos.clave,
    }
    usuarios.append(nuevo_usuario)
    return {
        "mensaje": "Usuario creado",
        "usuario": nuevo_usuario,
        "creado_por": usuario_actual,
    }


@router.put("/{usuario_id}")
def actualizar_usuario(
    usuario_id: int,
    datos: UsuarioEntrada,
    usuario_actual: dict = Depends(seguridad.obtener_usuario_actual),
):
    for usuario in usuarios:
        if usuario["id"] == usuario_id:
            usuario["nombre"] = datos.nombre
            usuario["correo"] = datos.correo
            usuario["clave"] = datos.clave
            return {
                "mensaje": "Usuario actualizado",
                "usuario": usuario,
                "modificado_por": usuario_actual,
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, admin: dict = Depends(seguridad.requerir_admin)):
    for usuario in usuarios:
        if usuario["id"] == usuario_id:
            usuarios.remove(usuario)
            return {
                "mensaje": "Usuario eliminado",
                "usuario": usuario,
                "eliminado_por": admin["username"],
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
