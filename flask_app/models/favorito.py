from flask_app.config.mysqlconnection import connectToMySQL

class Favorito:
    BASE_DE_DATOS = 'esquema_bookhub'

    def __init__(self, data):
        self.id = data['id']
        self.id_usuario = data['id_usuario']
        self.id_libro = data['id_libro']
        self.nombre_libro = data.get('nombre_libro')
        self.nombre_autor = data.get('nombre_autor')

    # CREATE: Vincular libro a favoritos (Maneja reactivación por soft delete)
    @classmethod
    def guardar(cls, data):
        query = "INSERT INTO favoritos (id_usuario, id_libro, created_by) VALUES (%(id_usuario)s, %(id_libro)s, %(created_by)s) ON DUPLICATE KEY UPDATE deleted = 0, updated_by = %(created_by)s;"
        return connectToMySQL(cls.BASE_DE_DATOS).query_db(query, data)

    # READ: Obtener favoritos activos vinculados al usuario con JOINs
    @classmethod
    def obtener_por_usuario(cls, id_usuario):
        query = "SELECT favoritos.*, libros.nombre AS nombre_libro, autores.nombre AS nombre_autor FROM favoritos JOIN libros ON favoritos.id_libro = libros.id JOIN autores ON libros.autor = autores.id WHERE favoritos.id_usuario = %(id_usuario)s AND favoritos.deleted = 0 AND libros.deleted = 0;"
        data = {'id_usuario': id_usuario}
        resultados = connectToMySQL(cls.BASE_DE_DATOS).query_db(query, data)
        return [cls(fila) for fila in resultados] if resultados else []

    # DELETE: Borrado lógico de favoritos
    @classmethod
    def borrar_logico(cls, id, usuario):
        query = "UPDATE favoritos SET deleted = 1, updated_by = %(updated_by)s WHERE id = %(id)s;"
        data = {'id': id, 'updated_by': usuario}
        return connectToMySQL(cls.BASE_DE_DATOS).query_db(query, data)
