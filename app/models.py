import datetime  # Importamos datetime
from flask_login import UserMixin
# Para generar hash en las contraseñas
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
# El '.' es una referencia al modulo principal (modulo de la app)
from . import db


# Usamos uso de ORM para creación del modelo User para la base de datos
# Heredamos de la clase 'UserMixin' para poder usar los métodos para las sesiones e identificación de usuarios
class User(db.Model, UserMixin):
    # Cambiamos el nombre de la tabla a 'users'
    __tablename__ = 'users'

    # Definimos las columnas
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(94), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    # lazy='dynamic' -> Nos servira para poder paginar las tareas, en este caso los objetos
    tasks = db.relationship('Task', lazy='dynamic')

    # Método para verificar el password
    # Se compara el password encriptado con el password que se recibe en el login
    def verify_password(self, password):
        return check_password_hash(self.encrypted_password, password)

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

    @classmethod
    def get_by_id(cls, id):
        # cls -> Es la misma instancia
        # id -> ID a validar
        # Realizamos una busqueda del id con 'query.filter_by'
        # Buscamos al id
        return User.query.filter_by(id=id).first()


# Modelo para las tareas
class Task(db.Model):
    # Cambiamos el nombre de la tabla
    __tablename__ = 'tasks'

    # Atributos para el modelo
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.Text())
    # Colocamos la llave foraneo para relacionar las tareas con el usuario que las creo
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    # Migraciones
    # En el caso de querer agregar nuevas columnas sin borrar los registros actuales, usamos migraciones
    # Nos apoyamos en la librería Flask-Migrate
    # Agregamos el campo 'updated_at'
    # Para agregar dicho campo es necesario ejecutar estos 3 comandos:
    # 'python manage.py db init' -> Para iniciar las migraciones
    # 'python manage.py db migrate' -> Realizar nuevas migraciones
    # 'python manage.py db upgrade' -> Realizar cambios en la base de datos
    updated_at = db.Column(db.DateTime)

    # Creamos una propiedad para acortar la descripción
    @property
    def little_description(self):
        # Si la descripción es mayor a 40 carácteres entonces la acortamos y le concatenamos '...'
        if len(self.description) > 40:
            return self.description[0:39] + "..."

        # Si no es mayor a 40 carácteres entonces la retornamos como esta
        return self.description

    # Método para crear tareas
    @classmethod
    def create_task(cls, title, description, user_id):
        # Creamos la tarea a través de su modelo
        task = Task(title=title, description=description, user_id=user_id)

        # Agregamos dicha tarea a la base de datos
        db.session.add(task)
        db.session.commit()

        # Retornamos la tarea
        return task

    # Método para obtener una tarea por su id
    @classmethod
    def get_by_id(cls, id):
        return Task.query.filter_by(id=id).first()

    # Método para actualizar una tarea
    @classmethod
    def update_task(cls, task_id, title, description):
        # Buscamos la tarea por su id
        task = Task.get_by_id(task_id)

        # Si la tarea esta vacía retorna False
        if task is None:
            return False

        # Colocamos los nuevos valores de la tarea
        task.title = title
        task.description = description

        # Agregamos dicha tarea a la base de datos
        db.session.add(task)
        db.session.commit()

        # Retornamos la tarea
        return task

    # Método para borrar una tarea
    @classmethod
    def delete_task(cls, task_id):
        # Buscamos la tarea por su id
        task = Task.get_by_id(task_id)

        # Si la tarea esta vacía retorna False
        if task is None:
            return False

        # Borramos la tarea en la base de datos
        db.session.delete(task)
        db.session.commit()

        # Retornamos True, dando a entender que todo paso correctamente
        return True
