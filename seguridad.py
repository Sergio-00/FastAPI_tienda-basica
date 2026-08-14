from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from database import obtener_conexion

# Configuracion (en un proyecto real, la clave va en una variable de entorno)
SECRET_KEY = "clave-super-secreta-de-mas-de-32-caracteres-cambieme"
ALGORITMO = "HS256"
MINUTOS_EXPIRACION = 30


# Hashing de contrasenas
def hashear_password(password: str) -> str:
    hasheado = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hasheado.decode()


def verificar_password(plano: str, hasheado: str) -> bool:
    return bcrypt.checkpw(plano.encode(), hasheado.encode())


def buscar_usuario(username: str):
    conexion = obtener_conexion()

    fila = conexion.execute(
        "SELECT * FROM usuarios WHERE username = ?",
        (username,),
    ).fetchone()

    conexion.close()

    return dict(fila) if fila else None


# Crear un token que guarda el usuario y su fecha de expiracion
def crear_token(username: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACION)
    return jwt.encode({"sub": username, "exp": expira}, SECRET_KEY, algorithm=ALGORITMO)


# Le dice a FastAPI donde se obtiene el token (activa el boton Authorize en /docs)
oauth2_esquema = OAuth2PasswordBearer(tokenUrl="auth/login")


# Dependencia: valida el token y devuelve el usuario. Si falla -> 401
def obtener_usuario_actual(token: str = Depends(oauth2_esquema)):
    error = HTTPException(
        status_code=401, detail="Token invalido", headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        datos = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITMO])
        username = datos.get("sub")
        if username is None:
            raise error
    except jwt.PyJWTError:
        raise error

    usuario = buscar_usuario(username)
    if usuario is None:
        raise error
    return usuario


# Dependencia: exige rol admin. Si no lo es -> 403
def requerir_admin(usuario: dict = Depends(obtener_usuario_actual)):
    if usuario["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Requiere rol de administrador")
    return usuario
