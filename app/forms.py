from wtforms import Form
from wtforms import validators
from wtforms import StringField, PasswordField


class LoginForm(Form):
    username = StringField('Username', [
        validators.DataRequired(message='Ingresa tu usuario'),
        validators.length(
            min=4, max=50, message='Mínimo deben ser 3 carácteres para el usuario'),
    ])
    password = PasswordField('Password', [
        validators.DataRequired(message='Ingresa una contraseña'),
        validators.length(
            min=4, max=50, message='Mínimo deben ser 3 carácteres para la contraseña')
    ])
