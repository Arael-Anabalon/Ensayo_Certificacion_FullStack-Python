from flask_app.config.mysqlconnection import connectToMySQL

class Autor:
    BASE_DE_DATOS = 'esquema_bookhub'

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.email = data['email']

    # CREATE: Insertar autor
    @classmethod
    def guardar(cls, data):
        query = "INSERT INTO autores (nombre, email, created_by) VALUES (%(nombre)s, %(email)s, %(created_by)s);"
        return connectToMySQL(cls.BASE_DE_DATOS).query_db(query, data)

    # READ: Obtener todos los autores activos
    @classmethod
    def obtener_todos(cls):
        query = "SELECT * FROM autores WHERE deleted = 0 ORDER BY nombre ASC;"
        resultados = connectToMySQL(cls.BASE_DE_DATOS).query_db(query)
        return [cls(fila) for fila in resultados] if resultados else []

    # DELETE: Borrado lógico de un autor
    @classmethod
    def borrar_logico(cls, id, usuario):
        query = "UPDATE autores SET deleted = 1, updated_by = %(updated_by)s WHERE id = %(id)s;"
        data = {'id': id, 'updated_by': usuario}
        return connectToMySQL(cls.BASE_DE_DATOS).query_db(query, data)
