from flask_app.config.mysqlconnection import connectToMySQL

class Libro:
    def __init__(self, db_conexion):
        self.db = db_conexion

    def crear(self, nombre, autor_id, descripcion, fecha, portada, creado_por, generos_ids):
        cursor = self.db.cursor()
        sql_libro = """INSERT INTO libros (nombre, autor, descripcion, fecha_publicacion, imagen_portada, created_by) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql_libro, (nombre, autor_id, descripcion, fecha, portada, creado_por))
        libro_id = cursor.lastrowid

        for g_id in generos_ids:
            cursor.execute("INSERT INTO libros_generos (id_libro, id_genero, created_by) VALUES (%s, %s, %s)", 
                           (libro_id, g_id, creado_por))
        self.db.commit()
        cursor.close()
        return libro_id

    def obtener_todos(self):
        cursor = self.db.cursor(dictionary=True)
        sql = """
            SELECT l.id, l.nombre, a.nombre AS autor, l.fecha_publicacion, l.created_by,
                   GROUP_CONCAT(g.nombre SEPARATOR ', ') AS generos,
                   (SELECT COUNT(*) FROM favoritos f WHERE f.id_libro = l.id AND f.deleted = 0) AS total_favoritos
            FROM libros l
            INNER JOIN autores a ON l.autor = a.id
            LEFT JOIN libros_generos lg ON l.id = lg.id_libro AND lg.deleted = 0
            LEFT JOIN generos g ON lg.id_genero = g.id AND g.deleted = 0
            WHERE l.deleted = 0 AND a.deleted = 0
            GROUP BY l.id ORDER BY l.created_at DESC;
        """
        cursor.execute(sql)
        libros = cursor.fetchall()
        cursor.close()
        return libros

    def obtener_por_id(self, libro_id):
        cursor = self.db.cursor(dictionary=True)
        sql = """
            SELECT l.*, a.nombre AS autor_nombre, GROUP_CONCAT(g.id) AS generos_ids, GROUP_CONCAT(g.nombre SEPARATOR ', ') AS generos
            FROM libros l
            INNER JOIN autores a ON l.autor = a.id
            LEFT JOIN libros_generos lg ON l.id = lg.id_libro AND lg.deleted = 0
            LEFT JOIN generos g ON lg.id_genero = g.id AND g.deleted = 0
            WHERE l.id = %s AND l.deleted = 0
            GROUP BY l.id;
        """
        cursor.execute(sql, (libro_id,))
        libro = cursor.fetchone()
        cursor.close()
        return libro

    def actualizar(self, libro_id, nombre, autor_id, descripcion, fecha, generos_ids, actualizado_por):
        cursor = self.db.cursor()
        sql_update = """UPDATE libros SET nombre = %s, autor = %s, descripcion = %s, fecha_publicacion = %s, updated_by = %s 
                        WHERE id = %s"""
        cursor.execute(sql_update, (nombre, autor_id, descripcion, fecha, actualizado_por, libro_id))

        cursor.execute("UPDATE libros_generos SET deleted = 1 WHERE id_libro = %s", (libro_id,))
        for g_id in generos_ids:
            cursor.execute("""INSERT INTO libros_generos (id_libro, id_genero, created_by) VALUES (%s, %s, %s) 
                              ON DUPLICATE KEY UPDATE deleted = 0""", (libro_id, g_id, actualizado_por))
        self.db.commit()
        cursor.close()

    def borrado_logico(self, libro_id, actualizado_por):
        cursor = self.db.cursor()
        cursor.execute("UPDATE libros SET deleted = 1, updated_by = %s WHERE id = %s", (actualizado_por, libro_id))
        self.db.commit()
        cursor.close()
