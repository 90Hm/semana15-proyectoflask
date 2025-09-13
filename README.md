# Proyecto Flask Continuación

## Instrucciones para ejecutar el proyecto

1. Abrir XAMPP y activar MySQL.
2. Importar `bd_proyecto_flask.sql` en phpMyAdmin.
3. Crear y activar el entorno virtual:

**Linux/macOS:**

```bash
.python3 -m venv venv
.source venv/bin/activate
.export FLASK_APP=app.py
.export FLASK_ENV=development
.flask run