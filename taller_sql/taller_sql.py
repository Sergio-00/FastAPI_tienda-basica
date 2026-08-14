import sqlite3
from pathlib import Path

#
# CONEXIÓN
#
# Carpeta donde está este archivo
conexion = sqlite3.connect(Path(__file__).parent / "taller.db")
cursor = conexion.cursor()

print("Base de datos conectada")

#
# 1. CREAR TABLA
#
cursor.execute("""
CREATE TABLE IF NOT EXISTS estudiantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    edad INTEGER,
    promedio REAL
)
""")

conexion.commit()

print("Tabla estudiantes creada")

#
# 2. INSERTAR DATOS
#
# Un registro con execute()
cursor.execute(
    """
INSERT INTO estudiantes (nombre, edad, promedio)
VALUES (?, ?, ?)
""",
    ("Ana", 20, 4.5),
)

# Varios registros con executemany()
datos = [
    ("Carlos", 22, 3.9),
    ("Luisa", 19, 4.8),
    ("Mateo", 25, 4.1),
    ("Sofia", 21, 4.7),
]

cursor.executemany(
    """
INSERT INTO estudiantes (nombre, edad, promedio)
VALUES (?, ?, ?)
""",
    datos,
)

conexion.commit()

print("Datos insertados correctamente")

#
# 3. CONSULTAS
#
print("\nTODOS LOS ESTUDIANTES")

cursor.execute("SELECT * FROM estudiantes")

for fila in cursor.fetchall():
    print(fila)

print("\nESTUDIANTES MAYORES DE 20")

cursor.execute("SELECT * FROM estudiantes WHERE edad > 20")

for fila in cursor.fetchall():
    print(fila)

print("\nORDENADOS POR PROMEDIO DESC")

cursor.execute("SELECT * FROM estudiantes ORDER BY promedio DESC")

for fila in cursor.fetchall():
    print(fila)

print("\nTOP 3 PROMEDIOS")

cursor.execute("SELECT * FROM estudiantes ORDER BY promedio DESC LIMIT 3")

for fila in cursor.fetchall():
    print(fila)

# fetchone()
print("\nPRIMER ESTUDIANTE (fetchone)")

cursor.execute("SELECT * FROM estudiantes")

primero = cursor.fetchone()

print(primero)

#
# 4. ACTUALIZAR Y ELIMINAR
#
cursor.execute(
    "UPDATE estudiantes SET promedio = ? WHERE id = ?",
    (5.0, 1),
)

conexion.commit()

print(f"\nFilas actualizadas: {cursor.rowcount}")

cursor.execute(
    "DELETE FROM estudiantes WHERE id = ?",
    (2,),
)

conexion.commit()

print(f"Filas eliminadas: {cursor.rowcount}")

#
# 5. LEER POR NOMBRE DE COLUMNA
#
conexion.row_factory = sqlite3.Row

cursor = conexion.cursor()

print("\nLECTURA POR NOMBRE DE COLUMNA")

cursor.execute("SELECT * FROM estudiantes LIMIT 1")

fila = cursor.fetchone()

print(f"Nombre: {fila['nombre']}")
print(f"Edad: {fila['edad']}")
print(f"Promedio: {fila['promedio']}")

print("Como diccionario:")
print(dict(fila))

#
# CIERRE
#
conexion.close()

print("\nConexión cerrada correctamente")
