from app import create_app
from flask_script import Manager
# Importamos el diccionario 'config'
from config import config

# Extraemos toda la parte de la llave 'development' del diccionario
config_class = config['development']

# Creamos la app pasando la configuración
app = create_app(config_class)


if __name__ == '__main__':
    # Usamos la clase Manager para correr la app
    manager = Manager(app)
    manager.run()
