from flask import Flask, render_template, request, redirect
from conexion.conexion import get_connection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/acerca')
def acerca():
    return render_template('acerca.html')

@app.route('/productos')
def productos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('productos.html', productos=productos)
@app.route('/clientes')
def clientes():
    buscar = request.args.get('buscar')
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if buscar:
        cursor.execute("SELECT * FROM clientes WHERE nombre LIKE %s", ('%' + buscar + '%',))
    else:
        cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

@app.route('/crear_cliente', methods=['GET', 'POST'])
def crear_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clientes (nombre, email) VALUES (%s, %s)",
            (nombre, email)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/clientes')
    return render_template('crear_cliente.html')

@app.route('/inventarios')
def inventarios():
    buscar = request.args.get('buscar')  # Captura el texto de búsqueda
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if buscar:
        cursor.execute("""
            SELECT p.id_producto, p.nombre, i.cantidad
            FROM inventarios i
            JOIN productos p ON i.id_producto = p.id_producto
            WHERE p.nombre LIKE %s
        """, ('%' + buscar + '%',))
    else:
        cursor.execute("""
            SELECT p.id_producto, p.nombre, i.cantidad
            FROM inventarios i
            JOIN productos p ON i.id_producto = p.id_producto
        """)

    inventarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('inventarios.html', inventarios=inventarios, buscar=buscar)


@app.route('/crear_producto', methods=['GET','POST'])
def crear_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        cantidad = request.form['cantidad']  # Cantidad inicial para inventario

        conn = get_connection()
        cursor = conn.cursor()

        # 1️⃣ Insertar en productos
        cursor.execute(
            "INSERT INTO productos (nombre, descripcion, precio) VALUES (%s, %s, %s)",
            (nombre, descripcion, precio)
        )
        conn.commit()

        # Obtener el ID del producto recién creado
        id_producto = cursor.lastrowid

        # 2️⃣ Insertar en inventarios con la cantidad
        cursor.execute(
            "INSERT INTO inventarios (id_producto, cantidad) VALUES (%s, %s)",
            (id_producto, cantidad)
        )
        conn.commit()

        cursor.close()
        conn.close()
        return redirect('/productos')  # Redirige a productos después de guardar

    return render_template('crear_producto.html')


if __name__ == '__main__':
    app.run(debug=True)
