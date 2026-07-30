from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/administradores", tags=["Administradores"])


class AdministradorEntrada(BaseModel):
    nombre: str
    correo: str
    clave: str
    nivel_permiso: str


administradores = [
    {
        "id": 1,
        "nombre": "Torres",
        "correo": "torres.admin@correo.com",
        "clave": "AdminSegura123",
        "nivel_permiso": "superadmin",
    },
    {
        "id": 2,
        "nombre": "Laura",
        "correo": "laura.admin@correo.com",
        "clave": "AdminLaura456",
        "nivel_permiso": "inventario",
    },
    {
        "id": 3,
        "nombre": "Andres",
        "correo": "andres.admin@correo.com",
        "clave": "AdminAndres789",
        "nivel_permiso": "ventas",
    },
]


@router.get("")
def listar_administradores():
    return administradores


@router.get("/{administrador_id}")
def obtener_administrador(administrador_id: int):
    for administrador in administradores:
        if administrador["id"] == administrador_id:
            return administrador
    raise HTTPException(status_code=404, detail="Administrador no encontrado")


@router.post("", status_code=201)
def crear_administrador(datos: AdministradorEntrada):
    nuevo_id = max((a["id"] for a in administradores), default=0) + 1

    nuevo_administrador = {
        "id": nuevo_id,
        "nombre": datos.nombre,
        "correo": datos.correo,
        "clave": datos.clave,
        "nivel_permiso": datos.nivel_permiso,
    }
    administradores.append(nuevo_administrador)
    return {
        "mensaje": "Administrador creado",
        "administrador": nuevo_administrador,
    }


@router.put("/{administrador_id}")
def actualizar_administrador(administrador_id: int, datos: AdministradorEntrada):
    for administrador in administradores:
        if administrador["id"] == administrador_id:
            administrador["nombre"] = datos.nombre
            administrador["correo"] = datos.correo
            administrador["clave"] = datos.clave
            administrador["nivel_permiso"] = datos.nivel_permiso
            return {
                "mensaje": "Administrador actualizado",
                "administrador": administrador,
            }
    raise HTTPException(status_code=404, detail="Administrador no encontrado")


@router.delete("/{administrador_id}")
def eliminar_administrador(administrador_id: int):
    for administrador in administradores:
        if administrador["id"] == administrador_id:
            administradores.remove(administrador)
            return {
                "mensaje": "Administrador eliminado",
                "administrador": administrador,
            }
    raise HTTPException(status_code=404, detail="Administrador no encontrado")
