from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "4e06af52370aef9777cc78cb672265e315cfe183429f8e1a8da5255a82fb5b02"
bcrypt = Bcrypt(app)

# Importar los planos independientes de los controladores
from flask_app.controllers.usuarios import usuarios_bp
from flask_app.controllers.libros import libros_bp
from flask_app.controllers.autores import autores_bp
from flask_app.controllers.generos import generos_bp
from flask_app.controllers.favoritos import favoritos_bp

# Registrar de forma centralizada cada enrutador
app.register_blueprint(usuarios_bp)
app.register_blueprint(libros_bp)
app.register_blueprint(autores_bp)
app.register_blueprint(generos_bp)
app.register_blueprint(favoritos_bp)
