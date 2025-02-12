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

### Auth

Gestión de autenticación:

- JWT
- DTOs
- Casos de uso (login)

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
- DTOs
- Casos de uso (crear usuario)

### Order

Gestión de órdenes:

- Modelos de dominio (Order, OrderItem)
- Repositorio abstracto
- Implementación PostgreSQL
- DTOs
- Casos de uso (crear orden, reportes)
- Validaciones de negocio

## Decisiones Técnicas

### Base de Datos

- PostgreSQL por consistencia y reportes
- Migraciones con Alembic vía scripts para facilitar la implementación en diferentes entornos
- Índices para en base de datos para optimización

**Tablas**

- **users:** id, name, email, password, created_at
- **orders:** id, customer_name, waiter_id, created_at
- **order_items:** id, order_id, product_name, unit_price, quantity, created_at

**Índice**

- **ix_users_email:** Índice para búsquedas por email (login y validaciones)
- **ix_order_items_product_stats:** Índice compuesto para reportes de ventas por producto y fecha

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
- Diagramas mermaid

### Diagramas

- [Arquitectura General](docs/diagrams/general_architecture.mmd)
- [Diagrama de Flujo de Autenticación](docs/diagrams/authentication_flow.mmd)
- [Diagrama de Flujo de Creación de Orden](docs/diagrams/order_creation_flow.mmd)
- [Modelo de Dominio](docs/diagrams/domain_model.mmd)
- [Flujo de Datos](docs/diagrams/data_flow.mmd)

### Estructura del Proyecto

```
backend-home-challenge/
├── alembic/                    # Configuración y migraciones de base de datos
│   ├── versions/               # Archivos de migración
│   └── env.py                  # Configuración del entorno de Alembic
│
├── container/                  # Archivos para construcción de Docker
│   ├── Dockerfile             # Definición de imagen
│   └── build.sh               # Script de construcción
│
├── docs/                       # Documentación del proyecto
│   └── diagrams/              # Diagramas de arquitectura y flujos
│
├── logs/                      # Archivos de log generados por la aplicación
│
├── scripts/                   # Scripts de utilidad
│   ├── db.py                 # CLI para gestión de base de datos
│   └── init_db.py            # Inicialización de base de datos
│
├── src/                       # Código fuente principal
│   ├── auth/                 # Módulo de autenticación
│   │   ├── application/      # Casos de uso y DTOs
│   │   └── infrastructure/   # Implementación JWT y rutas
│   │
│   ├── order/                # Módulo de órdenes
│   │   ├── application/      # Casos de uso y DTOs
│   │   ├── domain/          # Modelos y reglas de negocio
│   │   └── infrastructure/   # Repositorios y rutas
│   │
│   ├── shared/               # Componentes compartidos
│   │   ├── domain/          # Value objects y excepciones
│   │   ├── application/     # DTOs comunes
│   │   └── infrastructure/  # Configuración y middleware
│   │
│   ├── user/                # Módulo de usuarios
│   │   ├── application/     # Casos de uso y DTOs
│   │   ├── domain/         # Modelos y reglas de negocio
│   │   └── infrastructure/ # Repositorios y rutas
│   │
│   └── main.py             # Punto de entrada de la aplicación
│
├── tests/                   # Tests automatizados
│   ├── integration/        # Tests de integración
│   │   ├── api/           # Tests de endpoints
│   │   └── infrastructure/# Tests de repositorios
│   │
│   ├── unit/              # Tests unitarios
│   │   ├── application/   # Tests de casos de uso
│   │   └── domain/       # Tests de modelos y servicios
│   │
│   └── conftest.py        # Configuración y fixtures de pytest
│
├── .env.example           # Template de variables de entorno
├── .gitignore            # Archivos ignorados por git
├── alembic.ini           # Configuración de Alembic
├── pyproject.toml        # Configuración de herramientas Python
├── README.md             # Documentación principal
└── requirements.txt      # Dependencias del proyecto
```
