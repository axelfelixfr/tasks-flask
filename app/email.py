from flask_mail import Message
from flask import current_app, render_template
from threading import Thread
from . import mail, app


# Método para enviat el email de forma asincrona
def send_async_mail(message):
    # Creamos un contexto con 'app_context'
    with app.app_context():
        mail.send(message)


# Método para email de bienvenida (cuando se registre)
def welcome_mail(user):
    # Creamos el mensaje a través de la clase
    # sender -> Quien lo envia
    # recipients -> A quienes les llegara el correo (en este caso solo al usuario que se registra)
    message = Message('Bienvenido a TasksFlask',
                      sender=current_app.config['MAIL_USERNAME'],
                      recipients=[user.email])

    # A través de HTML construimos el mensaje y le pasamos el usuario
    message.html = render_template('email/welcome.html', user=user)

    # thread -> Ayudara a enviar el correo de forma asincrona
    # target -> El método que ejecutara de forma asincrona
    # args -> Los argumentos para ejecutar el método
    thread = Thread(target=send_async_mail, args=[message])

    # Con start() lo hacemos
    thread.start()
