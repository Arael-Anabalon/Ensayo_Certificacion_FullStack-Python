from flask import Blueprint, render_template, redirect, request, session, flash
from flask_app.models.libro import Libro
from flask_app.models.autor import Autor
from flask_app.models.genero import Genero

libros_bp = Blueprint('libros', __name__)

@libros_bp.route('/libros')
def galeria_libros():
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
    todos_libros = Libro.obtener_todos()
    return render_template('libros.html', libros=todos_libros)

@libros_bp.route('/libros/nuevo', methods=['GET', 'POST'])
def crear_libro():
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')

    if request.method == 'POST':
        data = {
            "nombre": request.form['nombre'],
            "autor": request.form['autor_id'],
            "descripcion": request.form['descripcion'],
            "fecha_publicacion": request.form['fecha_publicacion'],
            "imagen_portada": request.form.get('imagen_portada', ''),
            "created_by": session['usuario_nombre']
        }
        Libro.guardar(data)
        return redirect('/libros')

    autores = Autor.obtener_todos()
    return render_template('nuevo_libro.html', autores=autores)

@libros_bp.route('/libros/editar/<int:id>', methods=['GET', 'POST'])
def editar_libro(id):
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')

    resultado_libro = Libro.obtener_por_id(id)
    
    if not resultado_libro:
        return redirect('/libros')

    libro = resultado_libro[0] if isinstance(resultado_libro, list) else resultado_libro

    if request.method == 'POST':
        data = {
            "id": id,
            "nombre": request.form['nombre'],
            "autor": request.form['autor_id'],
            "descripcion": request.form['descripcion'],
            "fecha_publicacion": request.form['fecha_publicacion'],
            "imagen_portada": request.form.get('imagen_portada', ''),
            "updated_by": session['usuario_nombre']
        }
        Libro.actualizar(data)
        return redirect('/libros')

    autores = Autor.obtener_todos()
    generos_disponibles = Genero.obtener_todos()
    generos_libro = Libro.obtener_generos_asociados(id)
    return render_template('editar_libro.html', libro=libro, autores=autores, generos=generos_disponibles, generos_libro=generos_libro)

@libros_bp.route('/libros/asignar-genero', methods=['POST'])
def asignar_genero():
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
    data = {
        "id_libro": request.form['libro_id'],
        "id_genero": request.form['genero_id'],
        "created_by": session['usuario_nombre']
    }
    Libro.guardar_genero_asociado(data)
    return redirect(f"/libros/editar/{request.form['libro_id']}")

@libros_bp.route('/libros/quitar-genero/<int:id_libro>/<int:id_genero>')
def quitar_genero(id_libro, id_genero):
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
    Libro.borrar_genero_asociado(id_libro, id_genero, session['usuario_nombre'])
    return redirect(f"/libros/editar/{id_libro}")

@libros_bp.route('/libros/eliminar/<int:id>')
def eliminar_libro(id):
    if 'usuario_id' not in session:
        return redirect('/iniciar-sesion')
    Libro.borrar_logico(id, session['usuario_nombre'])
    return redirect('/libros')
