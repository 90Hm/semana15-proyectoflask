
# Sistema de Gestión de Productos, Inventarios y Clientes (Flask)

## Descripción
Este proyecto es una aplicación web hecha por un estudiante para la materia de Desarrollo de Aplicaciones Web. Permite gestionar productos, clientes e inventarios usando Python (Flask) y MySQL. Incluye autenticación de usuarios, registro, login y protección de rutas para que solo usuarios registrados puedan acceder a ciertas funciones.

## Funcionalidades principales
- Registro de usuarios y login seguro (contraseña encriptada).
- Solo los usuarios autenticados pueden ver y acceder a "Clientes" y "Crear Producto".
- Formularios modernos y personalizados para registro e inicio de sesión.
- Visualización y administración de productos, clientes e inventarios.
- Mensaje de bienvenida personalizado al iniciar sesión.
- Redirección automática para evitar que usuarios logueados vean los formularios de login o registro.

## Estructura del proyecto
- `app.py` → archivo principal de la aplicación Flask
- `conexion/conexion.py` → conexión a la base de datos MySQL
- `Models/ModelLogin.py` → modelo de usuario y funciones de autenticación
- `templates/` → HTML de todas las páginas (usa Jinja2)
- `static/css/estilo.css` → estilos personalizados
- `bd_proyecto_flask.sql` → script para crear la base de datos y tablas
- `requirements.txt` → dependencias de Python

## Requisitos
- Python 3.x
- Flask
- Flask-Login
- mysql-connector-python
- MySQL (XAMPP)

## Instalación y ejecución
1. Abre XAMPP y activa MySQL.
2. Importa la base de datos:
   - Abre phpMyAdmin y ejecuta/importa `bd_proyecto_flask.sql`.
3. Crea y activa un entorno virtual:
   - `python -m venv venv`
   - `venv\Scripts\activate` (Windows) o `source venv/bin/activate` (Linux/Mac)
4. Instala las dependencias:
   - `pip install -r requirements.txt`
5. Ejecuta la app:
   - `python app.py`

## Notas
- Para ver los apartados de "Clientes" y "Crear Producto" debes registrarte e iniciar sesión.
- Los usuarios no autenticados solo pueden ver la información general y los productos.

---
Hecho por: Brayan C. (estudiante)