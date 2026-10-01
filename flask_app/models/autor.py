from flask_app.config.mysqlconnection import connectToMySQL

class Autor:
    def __init__(self, db_conexion):
        self.db = db_conexion

    def crear(self, nombre, email, creado_por):
        cursor = self.db.cursor()
        sql = "INSERT INTO autores (nombre, email, created_by) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre, email, creado_por))
        nuevo_id = cursor.lastrowid
        self.db.commit()
        cursor.close()
        return nuevo_id

    def obtener_todos(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM autores WHERE deleted = 0 ORDER BY nombre ASC")
        autores = cursor.fetchall()
        cursor.close()
        return autores

    def obtener_por_id(self, autor_id):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM autores WHERE id = %s AND deleted = 0", (autor_id,))
        autor = cursor.fetchone()
        cursor.close()
        return autor

    def actualizar(self, autor_id, nombre, email, actualizado_por):
        cursor = self.db.cursor()
        sql = "UPDATE autores SET nombre = %s, email = %s, updated_by = %s WHERE id = %s"
        cursor.execute(sql, (nombre, email, actualizado_por, autor_id))
        self.db.commit()
        cursor.close()

    def borrado_logico(self, autor_id, actualizado_por):
        cursor = self.db.cursor()
        cursor.execute("UPDATE autores SET deleted = 1, updated_by = %s WHERE id = %s", (actualizado_por, autor_id))
        self.db.commit()
        cursor.close()
