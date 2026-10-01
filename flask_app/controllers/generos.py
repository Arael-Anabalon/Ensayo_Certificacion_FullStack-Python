from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_app.models.genero import Genero

generos_bp = Blueprint('generos', __name__, url_prefix='/generos')

@generos_bp.route('/')
def listar():
    if 'usuario_id' not in session: return redirect(url_for('usuarios.login_registro'))
    lista = Genero("esquema_bookhub").obtener_todos()
    return render_template('generos_lista.html', generos=lista)

@generos_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if 'usuario_id' not in session: return redirect(url_for('usuarios.login_registro'))
    if request.method == 'POST':
        Genero("esquema_bookhub").crear(request.form.get('nombre'), request.form.get('descripcion'), session['usuario_email'])
        return redirect(url_for('generos.listar'))
    return render_template('generos_nuevo.html')

@generos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'usuario_id' not in session: return redirect(url_for('usuarios.login_registro'))
    model = Genero("esquema_bookhub")
    if request.method == 'POST':
        model.actualizar(id, request.form.get('nombre'), request.form.get('descripcion'), session['usuario_email'])
        return redirect(url_for('generos.listar'))
    genero = model.obtener_por_id(id)
    return render_template('generos_editar.html', genero=genero)

@generos_bp.route('/borrar/<int:id>', methods=['POST'])
def borrar(id):
    if 'usuario_id' not in session: return redirect(url_for('usuarios.login_registro'))
    Genero("esquema_bookhub").borrado_logico(id, session['usuario_email'])
    return redirect(url_for('generos.listar'))
