import sqlite3
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from database import obtener_conexion
from models.modelos import RegistroEntrada
import seguridad

router = APIRouter(prefix="/auth", tags=["Autenticacion"])


@router.post("/registro", status_code=201)
def registrar_usuario(datos: RegistroEntrada):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO usuarios (username, nombre, password, rol)
            VALUES (?, ?, ?, ?)
            """,
            (
                datos.username,
                datos.nombre,
                seguridad.hashear_password(datos.password),
                "cliente",
            ),
        )

        conexion.commit()

    except sqlite3.IntegrityError:
        conexion.close()

        raise HTTPException(status_code=400, detail="El usuario ya existe")

    conexion.close()

    return {
        "mensaje": "Usuario registrado correctamente",
        "usuario": {
            "username": datos.username,
            "nombre": datos.nombre,
            "rol": "cliente",
        },
    }


# LOGIN: recibe un formulario usuario/contrasena y devuelve el token
@router.post("/login")
def login(datos: OAuth2PasswordRequestForm = Depends()):
    usuario = seguridad.buscar_usuario(datos.username)
    if usuario is None or not seguridad.verificar_password(
        datos.password, usuario["password"]
    ):
        raise HTTPException(status_code=401, detail="Usuario o contrasena incorrectos")
    token = seguridad.crear_token(usuario["username"])
    return {"access_token": token, "token_type": "bearer"}


# QUIEN SOY: endpoint protegido de ejemplo
@router.get("/yo")
def quien_soy(usuario: dict = Depends(seguridad.obtener_usuario_actual)):
    return {"username": usuario["username"], "rol": usuario["rol"]}
