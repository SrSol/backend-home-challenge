# Backend Home Challenge

## Descripción

Servicio REST para el challenge backend de Parrot Software.

## Stack

- [ ] [Python 3.9+](https://www.python.org/)
- [ ] [Fast API](https://fastapi.tiangolo.com/)
- [ ] [PostgreSQL 16+](https://www.postgresql.org/)
- [ ] [Docker (opcional)](https://www.docker.com/)

## Entornos

- **Localhost** localhost:8000/
- **Development** undefined
- **Production** undefined
- **Pruebas** undefined

## Building and running

### Instalación

Crear entorno virtual.

```bash
python -m venv venv

source venv/bin/activate # Linux/Mac

.\venv\Scripts\activate # Windows
```

Instala las dependencias del proyecto.

```bash
pip install -r requirements.txt
```

### Configuración inicial

Configurar variables de entorno.

```bash
cp .env.example .env
```

Editar el archivo `.env` con tus configuraciones.

Ejecutar migraciones.

```bash
python scripts/db.py init
```

Al ejecutar las migraciones se creará un usuario administrador por defecto:

- Email: admin@email.com
- Name: Admin

Este usuario puede ser utilizado para el primer inicio de sesión y configuración del sistema.

### Ejecución

Iniciar el servidor.

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `POST /api/v1/auth/login` - Login de usuario
- `GET /api/v1/users` - Listar usuarios
- `POST /api/v1/orders` - Crear orden
- `GET /api/v1/orders/report` - Reporte de ventas

Ver documentación completa en `/docs`

## Pruebas

Ejecutar todos los tests

```bash
pytest
```

Tests con cobertura

```bash
pytest --cov=src
```

Tests específicos

```bash
pytest tests/unit/
pytest tests/integration/
```

## Docker

### Build

Construir imagen.

```bash
docker build -t backend-home-challenge .
```

Ejecutar contenedor.

```bash
docker run -d -p 8000:8000 backend-home-challenge
```

## Migraciones

El proyecto incluye una herramienta CLI para la gestión de la base de datos:

```bash
# Inicializar la base de datos con migraciones
python scripts/db.py init

# Crear una nueva migración
python scripts/db.py create-migration "description"

# Aplicar migraciones pendientes
python scripts/db.py upgrade

# Revertir la última migración
python scripts/db.py downgrade

# Mostrar el estado de las migraciones
python scripts/db.py status

# Reiniciar la base de datos (cuidado!)
python scripts/db.py reset
```
