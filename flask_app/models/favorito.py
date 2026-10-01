from flask_app.config.mysqlconnection import connectToMySQL

class Favorito:
    def __init__(self, db_conexion):
        self.db = db_conexion

    def crear(self, usuario_id, libro_id, creado_por):
        cursor = self.db.cursor()
        sql = """INSERT INTO favoritos (id_usuario, id_libro, created_by) VALUES (%s, %s, %s)
                 ON DUPLICATE KEY UPDATE deleted = 0"""
        cursor.execute(sql, (usuario_id, libro_id, creado_por))
        self.db.commit()
        cursor.close()

    def obtener_por_usuario(self, usuario_id):
        cursor = self.db.cursor(dictionary=True)
        sql = """
            SELECT l.id, l.nombre, a.nombre AS autor, l.fecha_publicacion,
                   GROUP_CONCAT(g.nombre SEPARATOR ', ') AS generos
            FROM favoritos f
            INNER JOIN libros l ON f.id_libro = l.id
            INNER JOIN autores a ON l.autor = a.id
            LEFT JOIN libros_generos lg ON l.id = lg.id_libro AND lg.deleted = 0
            LEFT JOIN generos g ON lg.id_genero = g.id AND g.deleted = 0
            WHERE f.id_usuario = %s AND f.deleted = 0 AND l.deleted = 0
            GROUP BY l.id;
        """
        cursor.execute(sql, (usuario_id,))
        favs = cursor.fetchall()
        cursor.close()
        return favs

    def obtener_usuarios_por_libro(self, libro_id):
        cursor = self.db.cursor(dictionary=True)
        sql = """SELECT u.nombre, u.apellido FROM favoritos f 
                 INNER JOIN usuarios u ON f.id_usuario = u.id 
                 WHERE f.id_libro = %s AND f.deleted = 0 AND u.deleted = 0"""
        cursor.execute(sql, (libro_id,))
        usuarios = cursor.fetchall()
        cursor.close()
        return usuarios

    def es_favorito(self, usuario_id, libro_id):
        cursor = self.db.cursor(dictionary=True)
        sql = "SELECT id FROM favoritos WHERE id_usuario = %s AND id_libro = %s AND deleted = 0"
        cursor.execute(sql, (usuario_id, libro_id))
        res = cursor.fetchone()
        cursor.close()
        return res is not None

    def borrado_logico(self, usuario_id, libro_id, actualizado_por):
        cursor = self.db.cursor()
        sql = "UPDATE favoritos SET deleted = 1, updated_by = %s WHERE id_usuario = %s AND id_libro = %s"
        cursor.execute(sql, (actualizado_por, usuario_id, libro_id))
        self.db.commit()
        cursor.close()
