# Importamos la función create_app que realizamos en __init__
from app import create_app
from app import db, User, Task
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
# Importamos el diccionario 'config'
from config import config

# Extraemos toda la parte de la llave 'development' del diccionario
config_class = config['development']

# Creamos la app pasando la configuración
app = create_app(config_class)
# Instancia de Migrate
migrate = Migrate(app, db)


# Creamos el shell para la consola
def make_shell_context():
    # Retornamos el diccionario que tendra la shell
    return dict(app=app, db=db, User=User, Task=Task)


if __name__ == '__main__':
    # Usamos la clase Manager para correr la app
    manager = Manager(app)

    # Con manager podemos agregar un nuevo comando para realizar acciones con Python
    # En este caso, creamos el comando 'shell' con el contexto que se creo
    # Para correr el comando -> python manage.py shell
    manager.add_command('shell', Shell(make_context=make_shell_context))
    # Agregamos el comando 'db' para las migraciones
    # Ejemplo de comando de la librería Flask-Migrate -> python manage.py db init
    manager.add_command('db', MigrateCommand)

    # Otra forma de agregar comandos para la consola es con el decorador 'manager.command'
    # Para correr el comando -> python manage.py test
    @manager.command
    def test():
        # El nombre de la función, sera el nombre del comando, en este caso 'test'
        import unittest  # Importamos unittest para correr las pruebas
        # Guardamos las pruebas a realizar con TestLoader para cargar las pruebas y crear un wrapper
        tests = unittest.TestLoader().discover('tests')
        # Ejecutamos las pruebas con el método run() pasandole las pruebas
        unittest.TextTestRunner().run(tests)

    # Corremos la aplicación
    manager.run()
