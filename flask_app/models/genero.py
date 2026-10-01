from flask_app.config.mysqlconnection import connectToMySQL

class Genero:
    def __init__(self, db_conexion):
        self.db = db_conexion

    def crear(self, nombre, descripcion, creado_por):
        cursor = self.db.cursor()
        sql = "INSERT INTO generos (nombre, descripcion, created_by) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre, descripcion, creado_por))
        self.db.commit()
        cursor.close()

    def obtener_todos(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM generos WHERE deleted = 0 ORDER BY nombre ASC")
        generos = cursor.fetchall()
        cursor.close()
        return generos

    def obtener_por_id(self, genero_id):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM generos WHERE id = %s AND deleted = 0", (genero_id,))
        genero = cursor.fetchone()
        cursor.close()
        return genero

    def actualizar(self, genero_id, nombre, descripcion, actualizado_por):
        cursor = self.db.cursor()
        sql = "UPDATE generos SET nombre = %s, descripcion = %s, updated_by = %s WHERE id = %s"
        cursor.execute(sql, (nombre, descripcion, actualizado_por, genero_id))
        self.db.commit()
        cursor.close()

    def borrado_logico(self, genero_id, actualizado_por):
        cursor = self.db.cursor()
        cursor.execute("UPDATE generos SET deleted = 1, updated_by = %s WHERE id = %s", (actualizado_por, genero_id))
        self.db.commit()
        cursor.close()
