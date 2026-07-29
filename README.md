# API de la Tienda con FastAPI

La aplicación implementa una **API REST** organizada con **APIRouter**, validación de datos con **Pydantic** y operaciones **CRUD** para productos y categorías.

## Funcionalidades

### Productos

- `GET /productos` → listar productos
- `GET /productos/{id}` → obtener un producto
- `POST /productos` → crear un producto
- `PUT /productos/{id}` → actualizar un producto
- `DELETE /productos/{id}` → eliminar un producto

### Categorías

- `GET /categorias` → listar categorías
- `GET /categorias/{id}` → obtener una categoría
- `POST /categorias` → crear una categoría
- `PUT /categorias/{id}` → actualizar una categoría
- `DELETE /categorias/{id}` → eliminar una categoría

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/tienda-api.git
cd tienda-api
```

### 2. Crear el entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno

#### Con Git Bash:

```bash
source venv/Scripts/activate
```

### 4. Instalar dependencias

```bash
python -m pip install fastapi "uvicorn[standard]"
```

---

## Ejecutar la API

Desde la carpeta del proyecto:

```bash
python -m uvicorn main:app --reload
```

El servidor iniciará en:

```
http://127.0.0.1:8000
```

---

## Documentación

FastAPI genera automáticamente la documentación Swagger en:

```
http://127.0.0.1:8000/docs
```

---

## Ejemplo de petición POST

### Crear un producto

```json
{
  "nombre": "Auriculares Bluetooth",
  "precio": 180000,
  "categoria": "Audio"
}
```

### Crear una categoría

```json
{
  "nombre": "Consolas"
}
```
