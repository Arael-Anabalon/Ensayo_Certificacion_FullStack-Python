from flask_app.config.mysqlconnection import connectToMySQL

class Usuario:
    def __init__(self, db_conexion, bcrypt_instancia):
        self.db = db_conexion
        self.bcrypt = bcrypt_instancia

    def registrar(self, nombre, apellido, email, contrasena_plana):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT id FROM usuarios WHERE email = %s AND deleted = 0", (email,))
        if cursor.fetchone():
            cursor.close()
            return False
        
        contrasena_encriptada = self.bcrypt.generate_password_hash(contrasena_plana).decode('utf-8')
        sql = """INSERT INTO usuarios (nombre, apellido, email, contrasena, created_by) 
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (nombre, apellido, email, contrasena_encriptada, email))
        self.db.commit()
        cursor.close()
        return True

    def login(self, email, contrasena_plana):
        cursor = self.db.cursor(dictionary=True)
        sql = "SELECT * FROM usuarios WHERE email = %s AND deleted = 0"
        cursor.execute(sql, (email,))
        usuario = cursor.fetchone()
        cursor.close()
        
        if usuario and self.bcrypt.check_password_hash(usuario['contrasena'], contrasena_plana):
            return usuario
        return None

    def obtener_todos(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, apellido, email, created_at FROM usuarios WHERE deleted = 0")
        usuarios = cursor.fetchall()
        cursor.close()
        return usuarios

    def obtener_por_id(self, usuario_id):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, apellido, email FROM usuarios WHERE id = %s AND deleted = 0", (usuario_id,))
        usuario = cursor.fetchone()
        cursor.close()
        return usuario

    def actualizar(self, usuario_id, nombre, apellido, email, actualizado_por):
        cursor = self.db.cursor()
        sql = "UPDATE usuarios SET nombre = %s, apellido = %s, email = %s, updated_by = %s WHERE id = %s"
        cursor.execute(sql, (nombre, apellido, email, actualizado_por, usuario_id))
        self.db.commit()
        cursor.close()

    def borrado_logico(self, usuario_id, actualizado_por):
        cursor = self.db.cursor()
        cursor.execute("UPDATE usuarios SET deleted = 1, updated_by = %s WHERE id = %s", (actualizado_por, usuario_id))
        self.db.commit()
        cursor.close()
