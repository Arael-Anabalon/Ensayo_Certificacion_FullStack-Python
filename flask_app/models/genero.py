from flask_app.config.mysqlconnection import connectToMySQL

class Genero:
    BASE_DE_DATOS = 'esquema_bookhub'

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.descripcion = data['descripcion']

    @classmethod
    def guardar(cls, data):
        query = "INSERT INTO generos (nombre, descripcion, created_by) VALUES (%(nombre)s, %(descripcion)s, %(created_by)s);"
        return connectToMySQL(cls.BASE_DE_DATOS).query_db(query, data)

    @classmethod
    def obtener_todos(cls):
        query = "SELECT * FROM generos WHERE deleted = 0 ORDER BY nombre ASC;"
        resultados = connectToMySQL(cls.BASE_DE_DATOS).query_db(query)
        return [cls(fila) for fila in resultados] if resultados else []

    @classmethod
    def borrar_logico(cls, id, usuario):
        query = "UPDATE generos SET deleted = 1, updated_by = %(updated_by)s WHERE id = %(id)s;"
        data = {'id': id, 'updated_by': usuario}
        return connectToMySQL(cls.BASE_DE_DATOS).query_db(query, data)
