# API de la Tienda con FastAPI y SQLite3

API REST desarrollada con **FastAPI**, organizada con **APIRouter**, persistencia en **SQLite3** y autenticación **JWT**.

---

## Estructura del proyecto

```
tienda-api/
├── main.py
├── database.py
├── seguridad.py
├── requirements.txt
├── taller_sql/
│   ├── inyeccion_sql.py
│   ├── taller_sql.py
│   └── taller.db
├── models/
│   └── modelos.py
└── routers/
    ├── auth.py
    ├── productos.py
    ├── categorias.py
    ├── usuarios.py
    └── administradores.py
```

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Sergio-00/FastAPI_tienda-basica.git
cd FastAPI_tienda-basica
```

### 2. Crear el entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno

**Git Bash**

```bash
source venv/Scripts/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Ejecutar la API

```bash
python -m uvicorn main:app --reload
```

La aplicación estará disponible en:

```
http://127.0.0.1:8000
```

---

## Probar la API

FastAPI genera automáticamente la documentación interactiva:

```
http://127.0.0.1:8000/docs
```

### Flujo básico de prueba

1. Abrir `/docs`.
2. Pulsar **Authorize**.
3. Iniciar sesión como nombre admin y clave admin123.
4. Probar los endpoints sin proteger (`GET`) junto a los protegidos (`POST`, `PUT` y `DELETE`).

---

## Usuarios de ejemplo

| Usuario | Contraseña | Rol       | Permisos                                                            |
| ------- | ---------- | --------- | ------------------------------------------------------------------- |
| `admin` | `admin123` | `admin`   | Acceso completo, incluido `DELETE`                                  |
| `ana`   | `ana123`   | `cliente` | Puede consultar y modificar recursos autenticados, pero no eliminar |

---

## Endpoints principales

| Recurso                      | Métodos          |
| ---------------------------- | ---------------- |
| `/productos`                 | GET, POST        |
| `/productos/{id}`            | GET, PUT, DELETE |
| `/categorias`                | GET, POST        |
| `/categorias/{id}`           | GET, PUT, DELETE |
| `/categorias/{id}/productos` | GET              |
| `/auth/login`                | POST             |
| `/auth/registro`             | POST             |
| `/auth/yo`                   | GET              |

---

## Seguridad

- **GET** → acceso público.
- **POST** y **PUT** → requieren autenticación JWT.
- **DELETE** → requiere rol **admin**.

Las contraseñas se almacenan como **hash bcrypt**, nunca en texto plano.

---

## Base de datos

Al iniciar la aplicación se crea automáticamente el archivo **`tienda.db`** con las tablas:

- `categorias`
- `productos`
- `usuarios`

Los datos de ejemplo se insertan únicamente si la base de datos está vacía.
