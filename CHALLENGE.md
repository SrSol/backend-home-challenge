# Backend Home Challenge

¡Muchas gracias por participar!

En parrot buscamos crear un equipo de tecnología excelente. Por lo cual te pedimos que hagas tu mejor esfuerzo e incluyas técnicas y conocimientos que hagan brillar esta prueba.

## Areas a evaluar

- Conocimiento sobre APIs con estándar REST
- Conocimiento sobre bases de datos de alto consumo y disponibilidad
- Configuración de ambientes de desarrollo y deployment (Virtual Envs, Containers, etc...)
- Escalabilidad del código (que tan fácil es leerlo, mantenerlo, y probarlo)
- Resolución de requerimientos ambiguos (solución para temas con más de una respuesta correcta)

## Requerimientos Técnicos

- Que el proyecto se pueda desplegar de manera local
- Manejo y optimización de las consultas a una base de datos RELACIONAL
- Estricto uso del estándar REST
- Pruebas unitarias / integración (Solo para los WS)

## Requerimientos de Negocio

Se tiene que crear una API que será consumida por un conjunto de clientes (móviles y web).
El API será consumida por una base de 1000 usuarios con uso constante para la creación de ordenes.

Tiene que contener los siguientes servicios web, almacenando los datos necesarios para su correcto funcionamiento:

### 1. Creación de Usuarios-Meseros (Los usuarios no se podrán modificar una vez creados)

- Email (Llave única)
- Nombre
- No es necesario un password para el manejo de usuarios
- (Opcional) Obtener credenciales para consulta de todos los servicios que dependan del Usuario-Mesero. Todos los servicios web relacionados a un Usuario-Mesero deben estar protegidos por algún estándar de Autenticación.

### 2. Crear Ordenes para un Usuario-Comensal (Las ordenes serán creadas por el Usuario-Mesero)

- Nombre del Usuario-Comensal quien pidió la orden
- Precio Total de la orden
- Lista de Productos que conforman la Orden
- Las Ordenes deben contener la lista de Productos que la conforman. Los Productos son creados por el Usuario-Mesero al mismo tiempo que se crea la Orden. Productos con el mismo nombre será considerados como iguales.
  - Nombre del producto
  - Precio unitario
  - Cantidad

### 3. Reporte de productos vendidos

- Filtrado por fecha (inicio y fin)
- Ordenado por Producto de mayor a menor vendido
- Las Columnas necesarias para el reporte son: Nombre del producto, Cantidad Total, Precio Total

## Instrucciones

- Te recomendamos usar un proyecto base para que solo te enfoques en la funcionalidad del negocio
- El proyecto puede ser desarrollado con python o java/kotlin y con cualquier framework popular en ese lenguaje
- Contarás con 5 días hábiles para poder desarrollar el proyecto
- El proyecto se puede compartir a través de un repositorio de GitHub (o cualquier plataforma) o directamente por correo
- Te recomendamos usar lenguajes, prácticas y frameworks con los que te sientas muy cómodo, esperamos ver un proyecto listo para producción y usar tus mejores herramientas te ayudarán a alcanzar esa calidad
