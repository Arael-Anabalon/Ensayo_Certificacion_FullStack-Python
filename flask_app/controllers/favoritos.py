from flask import Blueprint, render_template, redirect, request, session, flash
from flask_app.models.favorito import Favorito

favoritos_bp = Blueprint('favoritos', __name__)

# CREATE: Añadir un libro a favoritos
@favoritos_bp.route('/favoritos/agregar', methods=['POST'])
def agregar_favorito():
    if 'usuario_id' not in session:
        flash("Inicia sesión para guardar favoritos.", "warning")
        return redirect('/iniciar-sesion')

    data = {
        "id_usuario": session['usuario_id'],
        "id_libro": request.form['libro_id'],
        "created_by": session['usuario_nombre']
    }
    Favorito.guardar(data)
    flash("Libro guardado en tus favoritos.", "success")
    return redirect('/libros')

# READ: Mostrar favoritos activos del usuario
@favoritos_bp.route('/favoritos')
def mis_favoritos():
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')

    libros_favoritos = Favorito.obtener_por_usuario(session['usuario_id'])
    return render_template('favoritos.html', favoritos=libros_favoritos)

# DELETE: Borrado lógico de favoritos
@favoritos_bp.route('/favoritos/eliminar/<int:id>')
def quitar_favorito(id):
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')

    Favorito.borrar_logico(id, session['usuario_nombre'])
    flash("El libro se quitó de tus favoritos.", "info")
    return redirect('/favoritos')
