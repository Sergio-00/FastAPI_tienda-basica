from fastapi import APIRouter, HTTPException, Depends
from database import obtener_conexion
from models.modelos import ProductoEntrada
import seguridad

# El router agrupa los endpoints de productos.
router = APIRouter(prefix="/productos", tags=["Productos"])


# GET - listar todos publico        GET /productos
@router.get("")
def listar_productos():
    conexion = obtener_conexion()

    filas = conexion.execute("SELECT * FROM productos").fetchall()

    conexion.close()

    return [dict(fila) for fila in filas]


# GET - obtener uno publico         GET /productos/{producto_id}
@router.get("/{producto_id}")
def obtener_producto(producto_id: int):
    conexion = obtener_conexion()

    fila = conexion.execute(
        "SELECT * FROM productos WHERE id = ?",
        (producto_id,),
    ).fetchone()

    conexion.close()

    if fila is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return dict(fila)


# POST - crear autenticado             POST /productos
@router.post("", status_code=201)
def crear_producto(
    datos: ProductoEntrada, usuario: dict = Depends(seguridad.obtener_usuario_actual)
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO productos (nombre, precio, categoria_id)
        VALUES (?, ?, ?)
        """,
        (
            datos.nombre,
            datos.precio,
            datos.categoria_id,
        ),
    )

    nuevo_id = cursor.lastrowid

    conexion.commit()
    conexion.close()

    return {
        "mensaje": "Producto creado",
        "producto": {
            "id": nuevo_id,
            **datos.model_dump(),
        },
        "creado_por": usuario["username"],
    }


# UPDATE - actualizar autenticado        PUT /productos/{producto_id}
@router.put("/{producto_id}")
def actualizar_producto(
    producto_id: int,
    datos: ProductoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        UPDATE productos
        SET nombre = ?, precio = ?, categoria_id = ?
        WHERE id = ?
        """,
        (
            datos.nombre,
            datos.precio,
            datos.categoria_id,
            producto_id,
        ),
    )

    if cursor.rowcount == 0:
        conexion.close()

        raise HTTPException(status_code=404, detail="Producto no encontrado")

    conexion.commit()
    conexion.close()

    return {
        "mensaje": "Producto actualizado",
        "producto": {
            "id": producto_id,
            **datos.model_dump(),
        },
        "modificado_por": usuario["username"],
    }


# DELETE - eliminar autenticado          DELETE /productos/{producto_id}
@router.delete("/{producto_id}")
def eliminar_producto(
    producto_id: int, admin: dict = Depends(seguridad.requerir_admin)
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM productos WHERE id = ?",
        (producto_id,),
    )

    if cursor.rowcount == 0:
        conexion.close()

        raise HTTPException(status_code=404, detail="Producto no encontrado")

    conexion.commit()
    conexion.close()

    return {
        "mensaje": "Producto eliminado",
        "producto_id": producto_id,
        "eliminado_por": admin["username"],
    }
