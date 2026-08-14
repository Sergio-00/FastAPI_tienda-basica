import sqlite3
from fastapi import APIRouter, HTTPException, Depends
from database import obtener_conexion
from models.modelos import CategoriaEntrada
import seguridad

router = APIRouter(prefix="/categorias", tags=["Categorias"])


# LISTAR (resuelto como ejemplo)
@router.get("")
def listar_categorias():
    conexion = obtener_conexion()

    filas = conexion.execute("SELECT * FROM categorias").fetchall()

    conexion.close()

    return [dict(fila) for fila in filas]


# GET  /categorias/{categoria_id}   -> obtener una (404 si no existe)
@router.get("/{categoria_id}")
def obtener_categoria(categoria_id: int):
    conexion = obtener_conexion()

    fila = conexion.execute(
        "SELECT * FROM categorias WHERE id = ?",
        (categoria_id,),
    ).fetchone()

    conexion.close()

    if fila is None:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    return dict(fila)


# POST /categorias               -> crear (status 201)
@router.post("", status_code=201)
def crear_categoria(
    datos: CategoriaEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "INSERT INTO categorias (nombre) VALUES (?)",
            (datos.nombre,),
        )

        nuevo_id = cursor.lastrowid

        conexion.commit()

    except sqlite3.IntegrityError:
        conexion.close()

        raise HTTPException(status_code=400, detail="La categoria ya existe")

    conexion.close()

    return {
        "mensaje": "Categoria creada",
        "categoria": {
            "id": nuevo_id,
            "nombre": datos.nombre,
        },
        "creado_por": usuario["username"],
    }


# PUT  /categorias/{categoria_id}   -> actualizar el nombre (404 si no existe)
@router.put("/{categoria_id}")
def actualizar_categoria(
    categoria_id: int,
    datos: CategoriaEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "UPDATE categorias SET nombre = ? WHERE id = ?",
        (datos.nombre, categoria_id),
    )

    if cursor.rowcount == 0:
        conexion.close()

        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    conexion.commit()
    conexion.close()

    return {
        "mensaje": "Categoria actualizada",
        "categoria": {
            "id": categoria_id,
            "nombre": datos.nombre,
        },
        "modificado_por": usuario["username"],
    }


# DELETE /categorias/{categoria_id} -> eliminar (404 si no existe)
@router.delete("/{categoria_id}")
def eliminar_categoria(
    categoria_id: int,
    admin: dict = Depends(seguridad.requerir_admin),
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Verificar si la categoria existe
    categoria = cursor.execute(
        "SELECT * FROM categorias WHERE id = ?",
        (categoria_id,),
    ).fetchone()

    if categoria is None:
        conexion.close()

        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    # Verificar si tiene productos asociados
    productos = cursor.execute(
        "SELECT COUNT(*) FROM productos WHERE categoria_id = ?",
        (categoria_id,),
    ).fetchone()[0]

    if productos > 0:
        conexion.close()

        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar la categoria porque tiene productos asociados",
        )

    cursor.execute(
        "DELETE FROM categorias WHERE id = ?",
        (categoria_id,),
    )

    conexion.commit()
    conexion.close()

    return {
        "mensaje": "Categoria eliminada",
        "categoria_id": categoria_id,
        "eliminado_por": admin["username"],
    }


# GET /categorias/{id}/productos
@router.get("/{categoria_id}/productos")
def obtener_categoria_con_productos(categoria_id: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    categoria = cursor.execute(
        "SELECT * FROM categorias WHERE id = ?",
        (categoria_id,),
    ).fetchone()

    if categoria is None:
        conexion.close()

        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    filas = cursor.execute(
        """
        SELECT
            id,
            nombre,
            precio,
            categoria_id
        FROM productos
        WHERE categoria_id = ?
        """,
        (categoria_id,),
    ).fetchall()

    conexion.close()

    return {
        "id": categoria["id"],
        "nombre": categoria["nombre"],
        "productos": [dict(fila) for fila in filas],
    }
