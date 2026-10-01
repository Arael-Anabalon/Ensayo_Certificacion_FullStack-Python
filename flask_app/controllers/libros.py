from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_app.models.libro import Libro
from flask_app.models.autor import Autor
from flask_app.models.genero import Genero
from flask_app.models.favorito import Favorito
from datetime import datetime

libros_bp = Blueprint('libros', __name__, url_prefix='/libros')

@libros_bp.route('/')
def mis_libros():
    if 'usuario_id' not in session: return redirect(url_for('usuarios.login_registro'))
    libros_activos = Libro("esquema_bookhub").obtener_todos()
    
    mis_libros = [l for l in libros_activos if l['created_by'] == session['usuario_email']]
    libros_comunidad = [l for l in libros_activos if l['created_by'] != session['usuario_email']]
    return render_template('libros.html', mis_libros=mis_libros, comunidad=libros_comunidad)

@libros_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if 'usuario_id' not in session: return redirect(url_for('usuarios.login_registro'))
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        autor_id = request.form.get('autor_id')
        generos = request.form.getlist('generos_ids')
        descripcion = request.form.get('descripcion')
        fecha = request.form.get('fecha_publicacion')

        if len(nombre) < 2 or not autor_id or not generos or len(descripcion) < 10:
            flash('Validaciones incorrectas', 'error')
        elif datetime.strptime(fecha, '%Y-%m-%d') > datetime.now():
            flash('Fecha inválida', 'error')
        else:
            Libro("esquema_bookhub").create(nombre, autor_id, descripcion, fecha, None, session['usuario_email'], generos)
            return redirect(url_for('libros.mis_libros'))
            
    autores = Autor("esquema_bookhub").obtener_todos()
    generos = Genero("esquema_bookhub").obtener_todos()
    return render_template('nuevo.html', autores=autores, generos=generos)

@libros_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'usuario_id' not in session: return redirect(url_for('usuarios.login_registro'))
    libro_model = Libro("esquema_bookhub")
    if request.method == 'POST':
        libro_model.actualizar(id, request.form.get('nombre'), request.form.get('autor_id'), request.form.get('descripcion'), request.form.get('fecha_publicacion'), request.form.getlist('generos_ids'), session['usuario_email'])
        return redirect(url_for('libros.mis_libros'))
    libro = libro_model.obtener_por_id(id)
    autores = Autor("esquema_bookhub").obtener_todos()
    generos = Genero("esquema_bookhub").obtener_todos()
    return render_template('nuevo.html', libro_editar=libro, autores=autores, generos=generos)

@libros_bp.route('/borrar/<int:id>', methods=['POST'])
def borrar(id):
    if 'usuario_id' not in session: return redirect(url_for('usuarios.login_registro'))
    Libro("esquema_bookhub").borrado_logico(id, session['usuario_email'])
    return redirect(url_for('libros.mis_libros'))

@libros_bp.route('/<int:id>')
def detalle(id):
    if 'usuario_id' not in session: return redirect(url_for('usuarios.login_registro'))
    libro = Libro("esquema_bookhub").obtener_por_id(id)
    ya_es_fav = Favorito("esquema_bookhub").es_favorito(session['usuario_id'], id)
    usuarios_fav = Favorito("esquema_bookhub").obtener_usuarios_por_libro(id)
    return render_template('libros.html', libro=libro, ya_es_fav=ya_es_fav, usuarios_fav=usuarios_fav)
