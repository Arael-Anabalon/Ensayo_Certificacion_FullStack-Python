from flask import Blueprint, render_template, redirect, url_for, session
from flask_app.models.favorito import Favorito

favoritos_bp = Blueprint('favoritos', __name__, url_prefix='/favoritos')

@favoritos_bp.route('/')
def mis_favoritos():
    if 'usuario_id' not in session: return redirect(url_for('usuarios.login_registro'))
    mis_favs = Favorito("esquema_bookhub").obtener_por_usuario(session['usuario_id'])
    return render_template('favoritos.html', favoritos=mis_favs)

@favoritos_bp.route('/agregar/<int:libro_id>', methods=['POST'])
def nuevo(libro_id):
    if 'usuario_id' not in session: return redirect(url_for('usuarios.login_registro'))
    Favorito("esquema_bookhub").crear(session['usuario_id'], libro_id, session['usuario_email'])
    return redirect(url_for('libros.detalle', id=libro_id))

@favoritos_bp.route('/borrar/<int:libro_id>', methods=['POST'])
def borrar(libro_id):
    if 'usuario_id' not in session: return redirect(url_for('usuarios.login_registro'))
    Favorito("esquema_bookhub").borrado_logico(session['usuario_id'], libro_id, session['usuario_email'])
    return redirect(url_for('libros.detalle', id=libro_id))
