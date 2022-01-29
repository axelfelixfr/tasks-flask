from flask import Flask
# Boostrap
from flask_bootstrap import Bootstrap
# CSRFProtect
from flask_wtf.csrf import CSRFProtect
# SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# LoginManager
from flask_login import LoginManager

# Realizamos una instancia
app = Flask(__name__)

# Realizamos la instancia de Bootstrap para los templates y el CSS
bootstrap = Bootstrap()
# Realizamos la instancia de CSRFProtect para la protección de formularios
csrf = CSRFProtect()
# Realizamos la instancia de SQLAlchemy para la base de datos
db = SQLAlchemy()
# Realizamos la instancia de LoginManager para identificar usuarios y generar sesiones
login_manager = LoginManager()


# Importamos page para las vistas
# Usamos '.' al tratarse de un archivo local en la misma dirección
from .views import page  # nopep8
from .models import User  # nopep8
from .consts import LOGIN_REQUIRED  # nopep8


# Creamos la función que crea la app
def create_app(config):
    # Usamos el método 'from_object' ya que se trata de un objeto/diccionario la configuración
    app.config.from_object(config)

    # Inicializamos Bootstrap
    bootstrap.init_app(app)

    # Inicializamos la seguridad CSRF
    csrf.init_app(app)

    # Inicializamos las sesiones e identificación de usuarios
    login_manager.init_app(app)

    # login_view -> Sera la página a la que sera redirigido si no tiene una sesión abierta
    login_manager.login_view = '.login'  # url_for
    # login_message -> Sera el mensaje que puede mostrar como error
    login_manager.login_message = LOGIN_REQUIRED
    # login_message_category -> Sera la categoría del mensaje, nos servira para la alerta de Bootstrap
    login_manager.login_message_category = 'warning'

    # Para las vistas, usamos 'register_blueprint'
    app.register_blueprint(page)

    # Creamos un contexto con 'app_context'
    with app.app_context():
        # Inicializamos SQLAlchemy
        db.init_app(app)
        # Creamos tablas
        db.create_all()

    # Retornamos la app
    return app
