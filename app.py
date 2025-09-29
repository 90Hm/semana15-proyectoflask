
# ...existing code...


import mysql.connector

# Función de conexión local a MySQL (XAMPP)
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='bd_proyecto_flask'  # Cambia si tu base tiene otro nombre
    )
from flask import session, flash
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from Models.ModelLogin import Usuario, obtener_por_email
from werkzeug.security import generate_password_hash



app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para sesiones y flash

# ========== VACIAR CARRITO ==========
@app.route('/vaciar_carrito', methods=['POST'])
def vaciar_carrito():
    user_id = str(current_user.id) if current_user.is_authenticated else 'anonimo'
    carritos = session.get('carritos', {})
    if not isinstance(carritos, dict):
        carritos = {}
    carritos[user_id] = {}
    session['carritos'] = carritos
    session.modified = True
    flash('Carrito vaciado correctamente')
    return redirect(url_for('carrito'))

# ========== HISTORIAL DE VENTAS PAGINADO ==========
@app.route('/historial_ventas')
@login_required
def historial_ventas():
    if not es_admin():
        flash('Solo los administradores pueden ver el historial de ventas.')
        return redirect(url_for('dashboard'))
    page = int(request.args.get('page', 1))
    per_page = 15
    offset = (page - 1) * per_page
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ventas")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT producto, cantidad, fecha, id_usuario FROM ventas ORDER BY fecha DESC LIMIT %s OFFSET %s", (per_page, offset))
    ventas = cursor.fetchall()
    cursor.close()
    conn.close()
    total_pages = (total + per_page - 1) // per_page
    return render_template('historial_ventas.html', ventas=ventas, page=page, total_pages=total_pages)

# ========== DASHBOARD ADMIN ==========
@app.route('/dashboard')
@login_required
def dashboard():
    if not es_admin():
        flash('Solo los administradores pueden acceder al panel de control.')
        return redirect(url_for('index'))
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total_usuarios = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total_clientes = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM productos")
    total_productos = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(cantidad) FROM inventarios")
    total_inventario = cursor.fetchone()[0] or 0
    productos_vendidos = 0
    historial_ventas = []
    ganancias = 0.0
    try:
        cursor.execute("SELECT SUM(cantidad) FROM ventas")
        productos_vendidos = cursor.fetchone()[0] or 0
        cursor.execute("SELECT producto, cantidad, fecha FROM ventas ORDER BY fecha DESC LIMIT 10")
        historial_ventas = [f"{row[0]} - {row[1]} unidades ({row[2]})" for row in cursor.fetchall()] if cursor.description else []
        # Calcular ganancias sumando precio * cantidad de cada venta
        cursor.execute("SELECT v.cantidad, p.precio FROM ventas v JOIN productos p ON v.producto = p.nombre")
        ventas = cursor.fetchall()
        for v in ventas:
            cantidad = v[0] or 0
            precio = float(v[1]) if v[1] is not None else 0.0
            ganancias += cantidad * precio
    except Exception:
        productos_vendidos = 0
        historial_ventas = []
        ganancias = 0.0
    cursor.close()
    conn.close()
    return render_template('dashboard.html', total_usuarios=total_usuarios, total_clientes=total_clientes, total_productos=total_productos, total_inventario=total_inventario, productos_vendidos=productos_vendidos, historial_ventas=historial_ventas, ganancias=ganancias)

# ========== ELIMINAR PRODUCTO ==========
@app.route('/eliminar_producto/<int:id_producto>', methods=['POST'])
def eliminar_producto(id_producto):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Producto eliminado correctamente')
    return redirect(url_for('productos'))

# ========== CARRITO DE COMPRAS ==========
@app.route('/agregar_carrito/<int:id_producto>', methods=['POST'])
def agregar_carrito(id_producto):
    # Si el usuario está autenticado, usar su id, si no, usar 'anonimo'
    user_id = str(current_user.id) if current_user.is_authenticated else 'anonimo'
    carritos = session.get('carritos', {})
    # Aseguramos que carritos sea dict simple
    if not isinstance(carritos, dict):
        carritos = {}
    carrito = carritos.get(user_id, {})
    if not isinstance(carrito, dict):
        carrito = {}
    key = str(id_producto)
    carrito[key] = carrito.get(key, 0) + 1
    carritos[user_id] = carrito
    session['carritos'] = carritos
    session.modified = True  # Fuerza guardar la sesión
    flash('Producto añadido al carrito')
    return redirect(url_for('productos'))

@app.route('/carrito')
def carrito():
    # Si el usuario está autenticado, usar su id, si no, usar 'anonimo'
    user_id = str(current_user.id) if current_user.is_authenticated else 'anonimo'
    carritos = session.get('carritos', {})
    if not isinstance(carritos, dict):
        carritos = {}
    carrito_raw = carritos.get(user_id, {})
    if not isinstance(carrito_raw, dict):
        carrito = {}
    else:
        carrito = dict(carrito_raw)
    productos_carrito = []
    cantidades = {}
    if carrito:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        id_list = [int(k) for k in carrito.keys() if carrito[k] > 0]
        if id_list:
            formato_ids = ','.join(['%s']*len(id_list))
            cursor.execute(f"SELECT * FROM productos WHERE id_producto IN ({formato_ids})", tuple(id_list))
            productos_carrito = cursor.fetchall()
            cantidades = {str(k): carrito[k] for k in carrito if carrito[k] > 0}
        cursor.close()
        conn.close()
    return render_template('carrito.html', productos=productos_carrito, cantidades=cantidades)
@app.route('/comprar_carrito', methods=['POST'])
def comprar_carrito():
    # Si el usuario no está autenticado, redirigir a login
    if not current_user.is_authenticated:
        flash('Debes iniciar sesión o registrarte para comprar productos.')
        return redirect(url_for('login_view'))
    user_id = str(current_user.id)
    carritos = session.get('carritos', {})
    carritos = dict(carritos) if isinstance(carritos, dict) else {}
    carrito_raw = carritos.get(user_id, {})
    if isinstance(carrito_raw, list):
        carrito = {}
        for id_producto in carrito_raw:
            key = str(id_producto)
            carrito[key] = carrito.get(key, 0) + 1
    else:
        carrito = dict(carrito_raw)
    if carrito:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        id_list = [int(k) for k in carrito.keys()]
        formato_ids = ','.join(['%s']*len(id_list))
        cursor.execute(f"SELECT * FROM productos WHERE id_producto IN ({formato_ids})", tuple(id_list))
        productos_carrito = cursor.fetchall()
        # Registrar la compra en la tabla ventas y actualizar inventario/productos
        cursor2 = conn.cursor()
        from datetime import datetime
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for producto in productos_carrito:
            cantidad = carrito[str(producto['id_producto'])]
            cursor2.execute(
                "INSERT INTO ventas (producto, cantidad, fecha, id_usuario) VALUES (%s, %s, %s, %s)",
                (producto['nombre'], cantidad, fecha, user_id)
            )
            # Actualizar inventario y productos
            cursor2.execute(
                "UPDATE inventarios SET cantidad = cantidad - %s WHERE id_producto = %s",
                (cantidad, producto['id_producto'])
            )
            cursor2.execute(
                "UPDATE productos SET cantidad = cantidad - %s WHERE id_producto = %s",
                (cantidad, producto['id_producto'])
            )
        conn.commit()
        cursor2.close()
        cursor.close()
        conn.close()
    # Vaciar solo el carrito del usuario actual
    carritos[user_id] = {}
    session['carritos'] = carritos
    mensaje = '¡Gracias por tu compra! En breve recibirás un correo electrónico con los detalles y la entrega de tus productos. Si tienes dudas, puedes contactarnos directamente desde la plataforma.'
    return render_template('confirmacion_carrito.html', productos=productos_carrito, mensaje=mensaje)
# ========== PAGO INDIVIDUAL DE PRODUCTO ==========
@app.route('/pagar_producto/<int:id_producto>', methods=['GET', 'POST'])
def pagar_producto(id_producto):
    if not current_user.is_authenticated:
        flash('Debes iniciar sesión o registrarte para comprar productos.')
        return redirect(url_for('login_view'))
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()
    if request.method == 'POST':
        # Registrar la compra en ventas y actualizar inventario/productos
        conn = get_connection()
        cursor = conn.cursor()
        from datetime import datetime
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO ventas (producto, cantidad, fecha, id_usuario) VALUES (%s, %s, %s, %s)",
            (producto['nombre'], 1, fecha, current_user.id)
        )
        cursor.execute(
            "UPDATE inventarios SET cantidad = cantidad - 1 WHERE id_producto = %s",
        )
        cursor.execute(
            "UPDATE productos SET cantidad = cantidad - 1 WHERE id_producto = %s",
            (id_producto,)
        )
        conn.commit()
        cursor.close()
        conn.close()
        mensaje = '¡Gracias por tu compra! En breve recibirás un correo electrónico con los detalles y la entrega de tus productos. Si tienes dudas, puedes contactarnos directamente desde la plataforma.'
        return render_template('confirmacion_pago.html', producto=producto, mensaje=mensaje)
    return render_template('pago.html', producto=producto)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# ==================== FLASK-LOGIN: USER LOADER ====================
@login_manager.user_loader
def load_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT idusuario, nombre, email, password, rol FROM usuarios WHERE idusuario = %s", (user_id,))
    fila = cursor.fetchone()
    cursor.close()
    conn.close()
    if fila:
        return Usuario(fila[0], fila[1], fila[2], fila[3], fila[4])
    return None

# ==================== RUTAS LOGIN / REGISTRO ====================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        rol = request.form.get('rol', 'usuario')

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s, %s, %s, %s)",
            (nombre, email, password, rol)
        )
        # Registrar también en clientes si es usuario normal
        if rol == 'usuario':
            cursor.execute(
                "INSERT INTO clientes (nombre, email) VALUES (%s, %s)",
                (nombre, email)
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
from flask_login import login_required
def es_admin():
    return current_user.is_authenticated and getattr(current_user, 'rol', None) == 'admin'

@app.route('/crear_producto', methods=['GET', 'POST'])
@login_required
def crear_producto():
    if not es_admin():
        flash('Solo los administradores pueden acceder a esta página.')
        return redirect(url_for('productos'))
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        descripcion = request.form.get('descripcion')
        cantidad = request.form.get('cantidad')
        if not cantidad:
            flash('El campo cantidad es obligatorio.')
            return render_template('crear_producto.html')
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, descripcion, precio, cantidad) VALUES (%s, %s, %s, %s)",
            (nombre, descripcion, precio, cantidad)
        )
        id_producto = cursor.lastrowid
        cursor.execute(
            "INSERT INTO inventarios (id_producto, cantidad) VALUES (%s, %s)",
            (id_producto, cantidad)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Producto creado correctamente')
        return redirect(url_for('productos'))
    return render_template('crear_producto.html')
@app.route('/')
def index():
    # Si el usuario es admin, pasar métricas
    if current_user.is_authenticated and getattr(current_user, 'rol', None) == 'admin':
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM clientes")
        total_clientes = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM productos")
        total_productos = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return render_template('index.html', total_usuarios=total_usuarios, total_clientes=total_clientes, total_productos=total_productos)
    return render_template('index.html')

@app.route('/acerca')
def acerca():
    return render_template('acerca.html')
    cursor.execute("DELETE FROM inventarios WHERE id_producto = %s", (id_producto,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Producto eliminado correctamente')
    return redirect(url_for('productos'))
@app.route('/productos')
def productos():
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) FROM productos")
    total_row = cursor.fetchone()
    total = list(total_row.values())[0] if total_row else 0
    cursor.execute("SELECT * FROM productos LIMIT %s OFFSET %s", (per_page, offset))
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    total_pages = (total + per_page - 1) // per_page
    return render_template('productos.html', productos=productos, page=page, total_pages=total_pages)

# ========== CRUD: EDITAR PRODUCTO ==========
@app.route('/editar_producto/<int:id_producto>', methods=['GET', 'POST'])
@login_required
def editar_producto(id_producto):
    if not es_admin():
        flash('Solo los administradores pueden acceder a esta página.')
        return redirect(url_for('productos'))
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        cantidad = request.form.get('cantidad')
        cursor.execute(
            "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, cantidad=%s WHERE id_producto=%s",
            (nombre, descripcion, precio, cantidad, id_producto)
        )
        cursor.execute(
            "UPDATE inventarios SET cantidad=%s WHERE id_producto=%s",
            (cantidad, id_producto)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Producto actualizado correctamente')
        return redirect(url_for('productos'))
    else:
        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
        producto = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('editar_producto.html', producto=producto)

@app.route('/clientes')
@login_required
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
@login_required
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
    if not es_admin():
        flash('Solo los administradores pueden acceder a esta página.')
        return redirect(url_for('index'))
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

# ==================== RUN ====================
if __name__ == '__main__':
    app.run(debug=True)
