import email_validator
from wtforms import Form
from wtforms import validators
from wtforms import StringField, PasswordField
from wtforms.fields.simple import EmailField, BooleanField

# Formulario de Login
class LoginForm(Form):
    # Para el login es necesario contar con: username, password
    # username sera un string, entonces se usa StringField
    username = StringField('Usuario', [
        # Array de validaciones
        # InputRequired -> Para que sea un campo obligatorio
        validators.InputRequired(message='Ingresa tu usuario'),
        # length -> Par definir el minimo y maximo de carácteres permitidos
        validators.length(
            min=4, max=50, message='Mínimo deben ser 4 carácteres para el usuario'),
    ])
    # password debe ser type password, entonces se usa PasswordField
    password = PasswordField('Contraseña', [
        validators.InputRequired(message='Ingresa una contraseña'),
        validators.length(
            min=4, message='Mínimo deben ser 4 carácteres para la contraseña')
    ])


# Formulario de Registro
class RegisterForm(Form):
    # Para el registro es necesario contar con: username, email, password, confirm_password, accept
    username = StringField('Usuario', [
        validators.InputRequired(message='Ingresa tu usuario'),
        validators.length(
            min=4, max=50, message='Mínimo deben ser 4 carácteres para el usuario')
    ])
    email = EmailField('Correo electrónico', [
        validators.length(
            min=6, max=50, message='Mínimo deben ser 6 carácteres para el correo electrónico'),
        validators.InputRequired(message='El correo electrónico es requerido'),
        # Email -> Para validar que el string sea un email
        validators.Email(message='El correo electrónico no es válido')
    ])
    password = PasswordField('Contraseña', [
        validators.InputRequired(message='La contraseña es requerida'),
        validators.length(
            min=4, message='Mínimo deben ser 4 carácteres para la contraseña'),
    ])
    confirm_password = PasswordField('Confirmar contraseña', [
        # EqualTo -> Para que sea igual al campo 'password'
        validators.EqualTo('password', message='La contraseña no coincide')
    ])
    # BooleanField -> Checkbox para aceptar los términos y condiciones
    # En este caso, se coloca un string vacío, ya que con el HTML le pondremos un label al campo
    accept = BooleanField('', [
        validators.InputRequired(
            message='Es necesario aceptar los términos y condiciones')
    ])
