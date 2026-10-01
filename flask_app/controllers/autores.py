from flask import Blueprint, render_template, redirect, request, session
from flask_app.models.autor import Autor

autores_bp = Blueprint('autores', __name__)

# READ: Listar todos los autores
@autores_bp.route('/autores')
def listar_autores():
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
    todos_autores = Autor.obtener_todos()
    return render_template('autores.html', autores=todos_autores)

# CREATE: Crear un nuevo autor
@autores_bp.route('/autores/nuevo', methods=['GET', 'POST'])
def nuevo_autor():
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')

    if request.method == 'POST':
        data = {
            "nombre": request.form['nombre'],
            "email": request.form['email'],
            "created_by": session['usuario_nombre']
        }
        Autor.guardar(data)
        return redirect('/libros/nuevo')
    return render_template('nuevo_autor.html')

# DELETE: Borrado lógico de un autor
@autores_bp.route('/autores/eliminar/<int:id>')
def eliminar_autor(id):
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
    Autor.borrar_logico(id, session['usuario_nombre'])
    return redirect('/autores')
