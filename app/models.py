import datetime  # Importamos datetime
# Para generar hash en las contraseñas
from werkzeug.security import generate_password_hash
# El '.' es una referencia al modulo principal (modulo de la app)
from . import db


# Usamos uso de ORM para creación del modelo User para la base de datos
class User(db.Model):
    # Cambiamos el nombre de la tabla a 'users'
    __tablename__ = 'users'

    # Definimos las columnas
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(94), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    # Se declara la propiedad password con el decorador 'property'
    @property
    def password(self):
        pass

    # Seteamos la propiedad password
    @password.setter
    def password(self, value):
        # Con self accedemos al registro y podemos acceder a sus propiedades (username, email, encrypted_password, etc)
        # Accedemos a la propiedad 'encrypted_password' para darle el valor del hash del password
        # Usamos la función generate_password_hash() para generar el password
        self.encrypted_password = generate_password_hash(value)

    # Sobreescribimos el método __str__
    # Esto es para que cuando llamemos la clase User, retornemos el username (el campo de base de datos)
    def __str__(self):
        # Retornamos unicamente el username
        return self.username

    # Creamos un método para la clase, usando el decorador 'classmethod'
    @classmethod
    def create_user(cls, username, email, password):
        # Creamos un usuario a través de su modelo y lo almacenamos en 'user'
        user = User(username=username, email=email, password=password)

        # Con 'db' de SQLAlchemy podemos acceder a 'session'
        # add() -> Agregar nuevo registro
        db.session.add(user)
        # commit -> Realizar cambio
        db.session.commit()

        # Retornamos el user creado
        return user

    # Métodos para validaciones de formulario
    # Usamos el decorador 'classmethod' en ambos casos
    @classmethod
    def get_by_username(cls, username):
        # cls -> Es la misma instancia
        # username -> Username a validar
        # Realizamos una busqueda del usuario con 'query.filter_by'
        # Buscamos al username
        return User.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        # cls -> Es la misma instancia
        # email -> Email a validar
        # Realizamos una busqueda del email con 'query.filter_by'
        # Buscamos al email
        return User.query.filter_by(email=email).first()
