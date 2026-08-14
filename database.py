import sqlite3
from seguridad import hashear_password

DB_NAME = "tienda.db"


def obtener_conexion():
    conexion = sqlite3.connect(DB_NAME, check_same_thread=False)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")

    return conexion


def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    #
    # TABLA CATEGORIAS
    #
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    )
    """)

    #
    # TABLA PRODUCTOS
    #
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        categoria_id INTEGER NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    )
    """)

    #
    # TABLA USUARIOS
    #
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        nombre TEXT NOT NULL,
        password TEXT NOT NULL,
        rol TEXT NOT NULL
    )
    """)

    conexion.commit()
    conexion.close()


def sembrar_datos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    #
    # CATEGORIAS
    #
    cursor.execute("SELECT COUNT(*) FROM categorias")

    if cursor.fetchone()[0] == 0:
        categorias = [
            ("Perifericos",),
            ("Pantallas",),
            ("Audio",),
        ]

        cursor.executemany(
            "INSERT INTO categorias (nombre) VALUES (?)",
            categorias,
        )

    #
    # PRODUCTOS
    #
    cursor.execute("SELECT COUNT(*) FROM productos")

    if cursor.fetchone()[0] == 0:
        productos = [
            ("Teclado mecanico", 120000, 1),
            ("Mouse gamer", 85000, 1),
            ("Monitor 24", 650000, 2),
        ]

        cursor.executemany(
            """
            INSERT INTO productos (nombre, precio, categoria_id)
            VALUES (?, ?, ?)
            """,
            productos,
        )

    #
    # USUARIOS
    #
    cursor.execute("SELECT COUNT(*) FROM usuarios")

    if cursor.fetchone()[0] == 0:
        usuarios = [
            (
                "admin",
                "Administrador",
                hashear_password("admin123"),
                "admin",
            ),
            (
                "ana",
                "Ana Cliente",
                hashear_password("ana123"),
                "cliente",
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO usuarios (username, nombre, password, rol)
            VALUES (?, ?, ?, ?)
            """,
            usuarios,
        )

    conexion.commit()
    conexion.close()
