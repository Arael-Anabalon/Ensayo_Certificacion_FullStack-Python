from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_bcrypt import Bcrypt
from flask_app.models.usuario import Usuario

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/', methods=['GET', 'POST'])
def login_registro():
    bcrypt = Bcrypt(current_app)
    if request.method == 'POST':
        usuario_model = Usuario("esquema_bookhub", bcrypt)
        accion = request.form.get('accion')

        if accion == 'registro':
            nombre = request.form.get('nombre')
            apellido = request.form.get('apellido')
            email = request.form.get('email')
            passw = request.form.get('contrasena')
            conf_passw = request.form.get('confirmar_contrasena')

            if len(nombre) < 2 or len(apellido) < 2:
                flash('Nombre y apellido mínimo 2 caracteres', 'error')
            elif passw != conf_passw:
                flash('Contraseñas no coinciden', 'error')
            else:
                if usuario_model.registrar(nombre, apellido, email, passw):
                    flash('Registro exitoso', 'success')
                else:
                    flash('El correo ya existe', 'error')

        elif accion == 'login':
            email = request.form.get('email')
            passw = request.form.get('contrasena')
            usuario = usuario_model.login(email, passw)
            if usuario:
                session['usuario_id'] = usuario['id']
                session['usuario_nombre'] = f"{usuario['nombre']} {usuario['apellido']}"
                session['usuario_email'] = usuario['email']
                return redirect(url_for('libros.mis_libros'))
            else:
                flash('Credenciales incorrectas', 'error')
    return render_template('iniciar_sesion.html')

@usuarios_bp.route('/usuarios')
def listar():
    if 'usuario_id' not in session: return redirect(url_for('usuarios.login_registro'))
    lista = Usuario("esquema_bookhub", None).obtener_todos()
    return render_template('usuarios_lista.html', usuarios=lista)

@usuarios_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'usuario_id' not in session: return redirect(url_for('usuarios.login_registro'))
    model = Usuario("esquema_bookhub", None)
    if request.method == 'POST':
        model.actualizar(id, request.form.get('nombre'), request.form.get('apellido'), request.form.get('email'), session['usuario_email'])
        return redirect(url_for('usuarios.listar'))
    user = model.obtener_por_id(id)
    return render_template('usuarios_editar.html', usuario=user)

@usuarios_bp.route('/usuarios/borrar/<int:id>', methods=['POST'])
def borrar(id):
    if 'usuario_id' not in session: return redirect(url_for('usuarios.login_registro'))
    Usuario("esquema_bookhub", None).borrado_logico(id, session['usuario_email'])
    return redirect(url_for('usuarios.listar'))

@usuarios_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('usuarios.login_registro'))
