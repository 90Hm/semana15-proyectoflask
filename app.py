from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from conexion.conexion import get_connection
from Models.ModelLogin import Usuario, obtener_por_email
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para sesiones y flash

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_view'  # Nombre de la función de login

# ==================== FLASK-LOGIN: USER LOADER ====================
@login_manager.user_loader
def load_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT idusuario, nombre, email, password FROM usuarios WHERE idusuario = %s", (user_id,))
    fila = cursor.fetchone()
    cursor.close()
    conn.close()
    if fila:
        return Usuario(fila[0], fila[1], fila[2], fila[3])
    return None

# ==================== RUTAS LOGIN / REGISTRO ====================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, password)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash('Usuario registrado correctamente')
        return redirect(url_for('login_view'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = obtener_por_email(email)
        if user and user.verificar_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos')
    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_view'))

# ==================== RUTAS EXISTENTES ====================
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

# ==================== RUN ====================
if __name__ == '__main__':
    app.run(debug=True)
