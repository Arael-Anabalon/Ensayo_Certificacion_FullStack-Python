from flask import Blueprint, render_template, redirect, request, session, flash
from flask_app.models.usuario import Usuario
from flask_app import bcrypt

usuarios_bp = Blueprint('usuarios', __name__)

# READ: Mostrar formulario de registro
@usuarios_bp.route('/')
def index():
    if 'usuario_id' in session:
        return redirect('/libros')
    return render_template('registrarse.html')

# READ: Mostrar formulario de login
@usuarios_bp.route('/iniciar-sesion')
def vista_login():
    if 'usuario_id' in session:
        return redirect('/libros')
    return render_template('iniciar_sesion.html')

# CREATE: Registrar nuevo usuario con contraseña encriptada
@usuarios_bp.route('/usuarios/registrar', methods=['POST'])
def procesar_registro():
    if not Usuario.validar_registro(request.form):
        return redirect('/')

    password_encriptada = bcrypt.generate_password_hash(request.form['contrasena']).decode('utf-8')
    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "contrasena": password_encriptada
    }
    usuario_id = Usuario.registrar(data)
    session['usuario_id'] = usuario_id
    session['usuario_nombre'] = f"{data['nombre']} {data['apellido']}"
    return redirect('/libros')

# READ: Procesar el inicio de sesión
@usuarios_bp.route('/usuarios/login', methods=['POST'])
def procesar_login():
    usuario = Usuario.obtener_por_email(request.form['email'])
    if not usuario or not bcrypt.check_password_hash(usuario.contrasena, request.form['contrasena']):
        flash("Credenciales incorrectas.", "danger")
        return redirect('/iniciar-sesion')

    session['usuario_id'] = usuario.id
    session['usuario_nombre'] = f"{usuario.nombre} {usuario.apellido}"
    return redirect('/libros')

# READ: Cerrar sesión limpia
@usuarios_bp.route('/usuarios/logout')
def logout():
    session.clear()
    return redirect('/iniciar-sesion')
