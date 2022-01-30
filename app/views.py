from flask import Blueprint
from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm, TaskForm
from .models import User, Task
from . import login_manager
from .consts import *
from .email import welcome_mail

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
    return render_template('auth/login.html', title='Inicio sesión', form=form, active='login')


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

            # Creamos la sesion
            login_user(user)

            # Enviamos el correo
            welcome_mail(user)

            return redirect(url_for('.tasks'))

    # Retornamos la vista junto con el form y title
    return render_template('auth/register.html', title='Registro', form=form, active='register')


# Ruta para las tareas
@page.route('/tasks')
@page.route('/tasks/<int:page>')  # Incluimos otra ruta para la paginación
# Decoramos con 'login_required' de LoginManager, para requerir estar logueado
@login_required
def tasks(page=1, per_page=4):  # page, per_page -> Paginación

    # Ahora con el current_user podemos acceder a sus tareas y paginarlas
    pagination = current_user.tasks.paginate(page, per_page)

    # Devolvera las tareas de acuerdo a la paginación
    tasks = pagination.items

    # Retornamos la vista de lista de tareas
    return render_template('tasks/list.html', title='Tareas', tasks=tasks, pagination=pagination, page=page, active='tasks')


# Ruta para crear una nueva tarea
@page.route('/tasks/new', methods=['GET', 'POST'])
@login_required
def new_task():
    # Instancia del formulario para crear tareas
    form = TaskForm(request.form)

    # Si la request es 'POST' y el formulario paso la validación, crea la tarea
    if request.method == 'POST' and form.validate():

        # Accedemos a title y description a través del 'form'
        title = form.title.data
        description = form.description.data

        # En cambio para id del usuario, usamos el current_user
        user_id = current_user.id

        # Creamos dicha tarea
        task = Task.create_task(title, description, user_id)

        # Si todo paso correctamente, devolvemos un mensaje y redirigimos a '/tasks'
        if task:
            flash(TASK_CREATED)
            return redirect(url_for('.tasks'))

    return render_template('tasks/new.html', title='Nueva tarea', form=form)


@page.route('/tasks/show/<int:task_id>')
@login_required
def get_task(task_id):
    task = Task.query.get_or_404(task_id)

    return render_template('tasks/show.html', title='Tarea', task=task)


@page.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    # Con la clase Task accedemos a 'get_or_404'
    # Con el método 'get_or_404' podremos obtener una tarea (task)
    task = Task.query.get_or_404(task_id)

    # Si la tarea no fue realizada por el mismo usuario que esta en sesion, manda un error 404
    if task.user_id != current_user.id:
        abort(404)

    # Podemos pasar la información (atributos de la BD) de la tarea con el 'obj'
    # Al 'obj' lo definimos como 'task' que obtuvimos
    form = TaskForm(request.form, obj=task)

    # Si la request es 'POST' y paso la validación el formulario hacemos la actualización
    if request.method == 'POST' and form.validate():
        # Actualizamos la tarea
        update_task = Task.update_task(
            task.id, form.title.data, form.description.data)

        # Si todo paso correctamente, mostramos un mensaje y redirigimos a '/tasks'
        if update_task:
            flash(TASK_UPDATE_SUCCESS)
            return redirect(url_for('.tasks'))

    # Retornamos la vista con el 'form' ya llenado
    return render_template('tasks/edit.html', title='Editar tarea', form=form)


# Ruta para eliminar una tarea
# En este caso es necesario contar con el parámetro 'task_id'
@page.route('/tasks/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    # Con el modelo Task, podemos buscar por el id
    task = Task.query.get_or_404(task_id)

    # Si la tarea no le pertenece al usuario, retorna un 404
    if task.user_id != current_user.id:
        abort(404)

    # Borra dicha tarea y regresa un mensaje
    if Task.delete_task(task.id):
        flash(TASK_DELETE_SUCCESS)

    return redirect(url_for('.tasks'))
