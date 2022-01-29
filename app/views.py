from flask import Blueprint
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm
from .models import User
from . import login_manager
from .consts import *

# Creamos una instancia de Blueprint para realizar vistas
page = Blueprint('page', __name__)


# Llamamos la instancia de LoginManager que esta en __init__
# Decoramos la función con 'user_loader'
@login_manager.user_loader
def load_user(id):
    # Buscamos al usuario por su id, con el méodo 'get_by_id'
    return User.get_by_id(id)


# Ahora con el decorador 'page.app_errorhandler()' podemos realizar una página con el error 404
# Es importante que en el decorador, pasemos el error a tratar como argumento
@page.app_errorhandler(404)
def page_not_found(error):  # Igual debemos pasar el error como argumento
    # Es obligatorio retornar dos argumentos
    # La pagina a retornar y el número del error que se trata
    return render_template('errors/404.html'), 404


# Index
@page.route('/')
def index():
    # Renderizamos la página principal, 'title' es una variable del template
    return render_template('index.html', title='Index')


# Logout
@page.route('/logout')
def logout():
    # 'logout_user' proviene de LoginManager para terminar la sesión
    logout_user()
    # Mandamos un mensaje por la vista
    flash(LOGOUT)
    # Con 'redirect' redirigimos al login
    return redirect(url_for('.login'))


# El method por default es 'GET' al momento de crear una route
# Ahora se coloca el method 'POST' para enviar el formulario
@page.route('/login', methods=['GET', 'POST'])
def login():

    # Con current_user accedemos al usuario actual
    # Comprobamos si esta autentificado, si lo esta, lo redirigimos a la url '/tasks'
    if current_user.is_authenticated:
        return redirect(url_for('.tasks'))

    # Realizamos una instancia de LoginForm
    # Accedemos a form de 'request'
    form = LoginForm(request.form)

    # Si el 'method' de la 'request' es POST y paso la validación pasa el if
    if request.method == 'POST' and form.validate():
        # Buscamos al usuario a través del método get_by_username
        user = User.get_by_username(form.username.data)

        # Después validamos la contraseña
        validate_password = user.verify_password(form.password.data)

        # Si ambas condiciones se cumplen, retorna una alerta de éxito
        if user and validate_password:
            login_user(user)
            flash(USER_LOGIN_SUCCESS)
            return redirect(url_for('.tasks'))
        else:
            flash(ERROR_USER_LOGIN, 'error')

    # Retornamos la vista, el title y el form para hacer uso de él
    return render_template('auth/login.html', title='Inicio sesión', form=form)


# Se coloca el method 'POST' para enviar el formulario
@page.route('/register', methods=['GET', 'POST'])
def register():

    # Con current_user accedemos al usuario actual
    # Comprobamos si esta autentificado, si lo esta, lo redirigimos a la url '/tasks'
    if current_user.is_authenticated:
        return redirect(url_for('.tasks'))

    # Instancia de formulario de registro
    form = RegisterForm(request.form)

    # Si el method de la request es 'POST'
    if request.method == 'POST':
        # Si pasa la validación del formulario
        if form.validate():
            # Extraemos cada elemento para crear el usuario del form
            username = form.username.data
            email = form.email.data
            password = form.password.data

            # Creamos el usuario, con el método 'create_user' del modelo 'User'
            user = User.create_user(username, email, password)

            # Con 'flash' podemos mostrar mensajes en la vista
            flash(USER_CREATED)

            login_user(user)

            return redirect(url_for('.tasks'))

    # Retornamos la vista junto con el form y title
    return render_template('auth/register.html', title='Registro', form=form)


# Ruta para las tareas
@page.route('/tasks')
# Decoramos con 'login_required' de LoginManager, para requerir estar logueado
@login_required
def tasks():
    # Retornamos la vista de lista de tareas
    return render_template('tasks/list.html', title='Tareas')
