from flask_app.config.mysqlconnection import connectToMySQL

class Libro:
    BASE_DE_DATOS = 'esquema_bookhub'

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.autor = data['autor']
        self.descripcion = data['descripcion']
        self.fecha_publicacion = data['fecha_publicacion']
        self.imagen_portada = data.get('imagen_portada')
        self.nombre_autor = data.get('nombre_autor')

    # CREATE: Insertar libro
    @classmethod
    def guardar(cls, data):
        query = "INSERT INTO libros (nombre, autor, descripcion, fecha_publicacion, imagen_portada, created_by) VALUES (%(nombre)s, %(autor)s, %(descripcion)s, %(fecha_publicacion)s, %(imagen_portada)s, %(created_by)s);"
        return connectToMySQL(cls.BASE_DE_DATOS).query_db(query, data)

    # READ: Obtener libros con INNER JOIN del autor activo
    @classmethod
    def obtener_todos(cls):
        query = "SELECT libros.*, autores.nombre AS nombre_autor FROM libros JOIN autores ON libros.autor = autores.id WHERE libros.deleted = 0 AND autores.deleted = 0;"
        resultados = connectToMySQL(cls.BASE_DE_DATOS).query_db(query)
        return [cls(fila) for fila in resultados] if resultados else []

    # READ: Obtener un libro por ID
    @classmethod
    def obtener_por_id(cls, id):
        query = "SELECT libros.*, autores.nombre AS nombre_autor FROM libros JOIN autores ON libros.autor = autores.id WHERE libros.id = %(id)s AND libros.deleted = 0;"
        data = {'id': id}
        resultados = connectToMySQL(cls.BASE_DE_DATOS).query_db(query, data)
        return cls(resultados[0]) if resultados else None

    # UPDATE: Modificar registro de libro
    @classmethod
    def actualizar(cls, data):
        query = "UPDATE libros SET nombre = %(nombre)s, autor = %(autor)s, descripcion = %(descripcion)s, fecha_publicacion = %(fecha_publicacion)s, imagen_portada = %(imagen_portada)s, updated_by = %(updated_by)s WHERE id = %(id)s;"
        return connectToMySQL(cls.BASE_DE_DATOS).query_db(query, data)

    # DELETE: Borrado lógico de un libro
    @classmethod
    def borrar_logico(cls, id, usuario):
        query = "UPDATE libros SET deleted = 1, updated_by = %(updated_by)s WHERE id = %(id)s;"
        data = {'id': id, 'updated_by': usuario}
        return connectToMySQL(cls.BASE_DE_DATOS).query_db(query, data)

    # CREATE: Asociar género a libro en tabla libros_generos (Maneja reactivación por soft delete)
    @classmethod
    def guardar_genero_asociado(cls, data):
        query = "INSERT INTO libros_generos (id_libro, id_genero, created_by) VALUES (%(id_libro)s, %(id_genero)s, %(created_by)s) ON DUPLICATE KEY UPDATE deleted = 0, updated_by = %(created_by)s;"
        return connectToMySQL(cls.BASE_DE_DATOS).query_db(query, data)

    # READ: Obtener géneros activos de este libro específico
    @classmethod
    def obtener_generos_asociados(cls, id_libro):
        query = "SELECT generos.* FROM generos JOIN libros_generos ON libros_generos.id_genero = generos.id WHERE libros_generos.id_libro = %(id_libro)s AND libros_generos.deleted = 0 AND generos.deleted = 0;"
        data = {'id_libro': id_libro}
        return connectToMySQL(cls.BASE_DE_DATOS).query_db(query, data)

    # DELETE: Soft delete de la relación género-libro
    @classmethod
    def borrar_genero_asociado(cls, id_libro, id_genero, usuario):
        query = "UPDATE libros_generos SET deleted = 1, updated_by = %(updated_by)s WHERE id_libro = %(id_libro)s AND id_genero = %(id_genero)s;"
        data = {'id_libro': id_libro, 'id_genero': id_genero, 'updated_by': usuario}
        return connectToMySQL(cls.BASE_DE_DATOS).query_db(query, data)
