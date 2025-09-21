
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from conexion.conexion import get_connection

class Usuario(UserMixin):
    def __init__(self, idusuario, nombre, email, password_hash):
        self.id = idusuario  # Flask-Login requiere self.id
        self.nombre = nombre
        self.email = email
        self.password_hash = password_hash

    def verificar_password(self, password):
        return check_password_hash(self.password_hash, password)

def obtener_por_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT idusuario, nombre, email, password FROM usuarios WHERE email = %s", (email,))
    fila = cursor.fetchone()
    cursor.close()
    conn.close()
    if fila:
        return Usuario(fila[0], fila[1], fila[2], fila[3])
    return None

