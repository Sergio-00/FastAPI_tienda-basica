from pydantic import BaseModel


#
# PRODUCTOS
#
class ProductoEntrada(BaseModel):
    nombre: str
    precio: float
    categoria_id: int


#
# CATEGORIAS
#
class CategoriaEntrada(BaseModel):
    nombre: str


#
# USUARIOS
#
class UsuarioEntrada(BaseModel):
    nombre: str
    correo: str
    clave: str


#
# ADMINISTRADORES
#
class AdministradorEntrada(BaseModel):
    nombre: str
    correo: str
    clave: str
    nivel_permiso: str


#
# AUTH
#
class RegistroEntrada(BaseModel):
    username: str
    nombre: str
    password: str
