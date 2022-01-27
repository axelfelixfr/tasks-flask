from ensurepip import bootstrap
from flask import Flask
# Importamos page para las vistas
# Usamos '.' al tratarse de un archivo local en la misma dirección
from .views import page
from flask_bootstrap import Bootstrap


# Realizamos una instancia
app = Flask(__name__)

bootstrap = Bootstrap()

# Creamos la función que crea la app


def create_app(config):
    # Usamos el método 'from_object' ya que se trata de un objeto/diccionario la configuración
    app.config.from_object(config)

    bootstrap.init_app(app)

    # Para las vistas, usamos 'register_blueprint'
    app.register_blueprint(page)

    # Retornamos la app
    return app
