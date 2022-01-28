from flask import Flask
# Boostrap
from flask_bootstrap import Bootstrap
# CSRFProtect
from flask_wtf.csrf import CSRFProtect
# SQLAlchemy
from flask_sqlalchemy import SQLAlchemy


# Realizamos una instancia
app = Flask(__name__)

# Realizamos la instancia de Bootstrap para los templates y el CSS
bootstrap = Bootstrap()
# Realizamos la instancia de CSRFProtect para la protección de formularios
csrf = CSRFProtect()
# Realizamos la instancia de SQLAlchemy para la base de datos
db = SQLAlchemy()

# Importamos page para las vistas
# Usamos '.' al tratarse de un archivo local en la misma dirección
from .views import page  # nopep8
from .models import User  # nopep8


# Creamos la función que crea la app
def create_app(config):
    # Usamos el método 'from_object' ya que se trata de un objeto/diccionario la configuración
    app.config.from_object(config)

    # Inicializamos Bootstrap
    bootstrap.init_app(app)

    # Inicializamos la seguridad CSRF
    csrf.init_app(app)

    # Para las vistas, usamos 'register_blueprint'
    app.register_blueprint(page)

    with app.app_context():
        # Inicializamos SQLAlchemy
        db.init_app(app)
        db.create_all()

    # Retornamos la app
    return app
