from flask import Blueprint, render_template, redirect, request, session
from flask_app.models.genero import Genero

generos_bp = Blueprint('generos', __name__)

# READ: Listar todos los géneros literarios
@generos_bp.route('/generos')
def listar_generos():
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
    todos_generos = Genero.obtener_todos()
    return render_template('generos.html', generos=todos_generos)

# CREATE: Crear un nuevo género
@generos_bp.route('/generos/nuevo', methods=['GET', 'POST'])
def nuevo_genero():
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')

    if request.method == 'POST':
        data = {
            "nombre": request.form['nombre'],
            "descripcion": request.form['descripcion'],
            "created_by": session['usuario_nombre']
        }
        Genero.guardar(data)
        return redirect('/generos')
    return render_template('nuevo_genero.html')

# DELETE: Borrado lógico de un género
@generos_bp.route('/generos/eliminar/<int:id>')
def eliminar_genero(id):
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
    Genero.borrar_logico(id, session['usuario_nombre'])
    return redirect('/generos')
