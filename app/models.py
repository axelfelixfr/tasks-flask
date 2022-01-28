import datetime  # Importamos datetime
# El '.' es una referencia al modulo principal (modulo de la app)
from . import db


# Usamos uso de ORM para creación del modelo User para la base de datos
class User(db.Model):
    # Cambiamos el nombre de la tabla a 'users'
    __tablename__ = 'users'

    # Definimos las columnas
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(93), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    # Sobreescribimos el método __str__
    # Esto es para que cuando llamemos la clase User, retornemos el username (el campo de base de datos)
    def __str__(self):
        return self.username
