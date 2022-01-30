import unittest
from flask import current_app
from app import db, User, Task
from app import create_app
from config import config


# Clase para pruebas
class DemoTestCase(unittest.TestCase):

    # setUp -> Acciones antes de ejecutar la prueba
    def setUp(self):
        config_class = config['test']
        self.app = create_app(config_class)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.id = 1

    # tearDown -> Acciones después de ejecutar la prueba
    def tearDown(self):
        # Eliminamos la sesion
        db.session.remove()

        # Después de cada prueba, eliminamos la información de la base de datos
        db.drop_all()

        # Eliminamos el contexto de la app
        self.app_context.pop()

    # Test de prueba
    def test_demo(self):
        self.assertTrue(1 == 1)

    # Test para comprobar que exista el usuario con id = 1
    def test_user_exists(self):
        # Buscamos el usuario a través de su id
        user = User.get_by_id(self.id)
        # Debe retornar None porque no hemos ingresado a la base de datos dicho usuario
        self.assertTrue(user is None)

    # Test para comprobar que se inserto un usuario en la BD
    def test_create_user(self):
        # Creamos el usuario con create_user
        user = User.create_user('axelf', 'axelf@correo.com', 'password')
        # Comprobamos que su id sea igual a '1' porque es el primer usuario que se inserta
        self.assertTrue(user.id == self.id)
