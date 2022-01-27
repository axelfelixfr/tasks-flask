from flask import Blueprint
from flask import render_template

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
    return render_template('index.html', title='Index')
