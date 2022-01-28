from flask import Blueprint
from flask import render_template, request
from .forms import LoginForm
# Creamos una instancia de Blueprint para realizar vistas
page = Blueprint('page', __name__)


# Ahora con el decorador 'page.app_errorhandler()' podemos realizar una página con el error 404
# Es importante que en el decorador, pasemos el error a tratar como argumento
@page.app_errorhandler(404)
def page_not_found(error):  # Igual debemos pasar el error como argumento
    # Es obligatorio retornar dos argumentos
    # La pagina a retornar y el número del error que se trata
    return render_template('errors/404.html'), 404


@page.route('/')
def index():
    # Renderizamos la página principal, 'title' es una variable del template
    return render_template('index.html', title='Index')


# El method por default es 'GET' al momento de crear una route
# Ahora se coloca el method 'POST' para enviar el formulario
@page.route('/login', methods=['GET', 'POST'])
def login():
    # Realizamos una instancia de LoginForm
    # Accedemos a form de 'request'
    form = LoginForm(request.form)

    # Si el 'method' de la 'request' es POST y paso la validación pasa el if
    if request.method == 'POST' and form.validate():
        print(form.username.data)
        print(form.password.data)

        print('Nueva sesión creada')

    # Retornamos la vista, el title y el form para hacer uso de él
    return render_template('auth/login.html', title='Login', form=form)
