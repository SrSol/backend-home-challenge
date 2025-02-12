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
- `POST /api/v1/users` - Crear usuario
- `POST /api/v1/orders` - Crear orden
- `GET /api/v1/orders/report` - Reporte de ventas

Ver documentación completa en `/docs`

## Pruebas

Ejecutar todos los tests

```bash
pytest
```

Tests específicos

```bash
pytest tests/unit/
pytest tests/integration/
```

## Docker

### Build

Construir imagen. Entrar a la carpeta `container` y ejecutar el script `build.sh`.

```bash
./build.sh
```

Ejecutar contenedor.

```bash
docker run -p 8000:8000 backend-home-challenge
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

## Arquitectura

### Visión General

El proyecto implementa Clean Architecture con las siguientes capas:

1. **Domain**: Reglas de negocio y modelos
2. **Application**: Casos de uso
3. **Infrastructure**: Implementaciones técnicas

### Módulos

### Shared

Componentes reutilizables:

- Value Objects (Email, Money)
- Excepciones de dominio
- Configuración
- Middleware
- Utilidades

### User

Gestión de usuarios:

- Modelo de dominio (User)
- Repositorio abstracto
- Implementación PostgreSQL
- DTOs y mappers
- Casos de uso (crear usuario)

### Order

Gestión de órdenes:

- Modelos (Order, OrderItem)
- Repositorio
- Casos de uso (crear orden, reportes)
- Validaciones de negocio

## Flujo de Datos

1. Request HTTP → FastAPI
2. Controller/Route → DTO
3. Command/Query → Domain Service
4. Repository → Database
5. Response ← DTO ← Entity

## Decisiones Técnicas

### Base de Datos

- PostgreSQL por consistencia y reportes
- Migraciones con Alembic
- Índices para optimización

**Tablas**

- users: id, name, email, password, created_at, updated_at
- orders: id, user_id, total_amount, created_at, updated_at
- order_items: id, order_id, product_id, quantity, price, created_at, updated_at

**Índice**

- ix_users_email: Índice para búsquedas por email (login y validaciones)

- ix_order_items_product_stats: Índice compuesto para reportes de ventas por producto y fecha

### Autenticación

- JWT stateless
- Sin refresh tokens
- Validación por email

### Testing

- Fixtures compartidos
- Base de datos SQLite en memoria
- Mocks estratégicos

### API

- REST con FastAPI
- Validación Pydantic
- Documentación OpenAPI
- Mermaid para diagramas

### Diagramas

- [Arquitectura General](docs/diagrams/general_architecture.mmd)
- [Diagrama de Flujo de Autenticación](docs/diagrams/authentication_flow.mmd)
- [Diagrama de Flujo de Creación de Orden](docs/diagrams/order_creation_flow.mmd)
- [Modelo de Dominio](docs/diagrams/domain_model.mmd)
- [Estructura de Carpetas](docs/diagrams/folder_structure.mmd)
- [Flujo de Datos](docs/diagrams/data_flow.mmd)
