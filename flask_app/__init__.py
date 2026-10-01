from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'tu_llave_secreta_para_sesiones_bookhub'

bcrypt = Bcrypt(app)

from flask_app.controllers.usuarios import usuarios_bp
from flask_app.controllers.libros import libros_bp
from flask_app.controllers.favoritos import favoritos_bp
from flask_app.controllers.autores import autores_bp
from flask_app.controllers.generos import generos_bp

app.register_blueprint(usuarios_bp)
app.register_blueprint(libros_bp)
app.register_blueprint(favoritos_bp)
app.register_blueprint(autores_bp)
app.register_blueprint(generos_bp)
