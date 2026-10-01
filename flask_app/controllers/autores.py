from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from flask_app.models.autor import Autor

autores_bp = Blueprint('autores', __name__, url_prefix='/autores')

@autores_bp.route('/')
def listar():
    if 'usuario_id' not in session: return redirect(url_for('usuarios.login_registro'))
    lista = Autor("esquema_bookhub").obtener_todos()
    return render_template('autores_lista.html', autores=lista)

@autores_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if 'usuario_id' not in session: return redirect(url_for('usuarios.login_registro'))
    if request.method == 'POST':
        Autor("esquema_bookhub").crear(request.form.get('nombre'), request.form.get('email'), session['usuario_email'])
        return redirect(url_for('autores.listar'))
    return render_template('autores_nuevo.html')

@autores_bp.route('/crear_ajax', methods=['POST'])
def crear_autor_ajax():
    if 'usuario_id' not in session: return jsonify({'error': 'No autorizado'}), 401
    datos = request.get_json()
    nombre_autor = datos.get('nombre')
    if not nombre_autor or len(nombre_autor.strip()) < 2: return jsonify({'error': 'Inválido'}), 400
    nuevo_id = Autor("esquema_bookhub").crear(nombre_autor.strip(), "comunidad@bookhub.com", session['usuario_email'])
    return jsonify({'id': nuevo_id, 'nombre': nombre_autor}), 201

@autores_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'usuario_id' not in session: return redirect(url_for('usuarios.login_registro'))
    model = Autor("esquema_bookhub")
    if request.method == 'POST':
        model.actualizar(id, request.form.get('nombre'), request.form.get('email'), session['usuario_email'])
        return redirect(url_for('autores.listar'))
    autor = model.obtener_por_id(id)
    return render_template('autores_editar.html', autor=autor)

@autores_bp.route('/borrar/<int:id>', methods=['POST'])
def borrar(id):
    if 'usuario_id' not in session: return redirect(url_for('usuarios.login_registro'))
    Autor("esquema_bookhub").borrado_logico(id, session['usuario_email'])
    return redirect(url_for('autores.listar'))
