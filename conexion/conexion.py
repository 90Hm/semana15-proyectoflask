import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",        # deja vacío si tu XAMPP no tiene contraseña
        database="bd_proyecto_flask"
    )
