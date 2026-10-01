import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    BASE_DE_DATOS = 'esquema_bookhub'

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.contrasena = data['contrasena']

    # CREATE: Insertar un usuario
    @classmethod
    def registrar(cls, data):
        query = "INSERT INTO usuarios (nombre, apellido, email, contrasena, created_by) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(contrasena)s, %(nombre)s);"
        return connectToMySQL(cls.BASE_DE_DATOS).query_db(query, data)

    # READ: Buscar usuario por email excluyendo borrados
    @classmethod
    def obtener_por_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s AND deleted = 0;"
        data = {'email': email}
        resultados = connectToMySQL(cls.BASE_DE_DATOS).query_db(query, data)
        return cls(resultados[0]) if resultados else None

    # READ: Validación de campos en el servidor
    @staticmethod
    def validar_registro(formulario):
        es_valido = True
        if len(formulario['nombre'].strip()) < 2:
            flash("Nombre muy corto.", "danger")
            es_valido = False
        if not EMAIL_REGEX.match(formulario['email']):
            flash("Email inválido.", "danger")
            es_valido = False
        if len(formulario['contrasena']) < 6:
            flash("Contraseña muy corta.", "danger")
            es_valido = False
        return es_valido
