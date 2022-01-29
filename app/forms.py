import email_validator
from wtforms import Form
from wtforms import validators
from wtforms import StringField, PasswordField, HiddenField
from wtforms.fields.simple import EmailField, BooleanField
from .models import User


# Validaciones mediante funciones
# Creamos la función 'admin_validator' que valide que ningún usuario se registre con el nombre 'admin'
def admin_validator(form, field):
    # Es obligatorio pasar dos parámetros: form, field
    # En este caso accedemos al valor del input con 'field.data'
    if field.data == 'admin' or field.data == 'Admin':
        # raise -> Podemos lanzar una excepción para mostrar el mensaje de error
        # ValidationError -> Mostrar un mensaje de error
        raise validators.ValidationError(
            'El username admin no puede ser utilizado')


# Honeypot un método anti spam
'''
Una de las formas en las cuales podemos prevenir el spam en nuestro sitio web es utilizando una 
pequeña técnica conocida como honeypot (tarro de miel). Esta técnica consiste, principalmente, en colocar 
un pequeño señuelo con el fin que un posible atacante caiga en él y de esta forma proteger nuestro sistema.
'''


def length_honeypot(form, field):
    # Es obligatorio pasar dos parámetros: form, field
    # Agregamos una pequeña validación a nuestro campo. Si el campo contiene algún valor levantamos un error
    if len(field.data) > 0:
        '''
         Si algún tipo de bot quiere generar usuarios inválidos hará la petición enviando valores para todos los 
         campos (No sabrá diferenciar entre un campo oculto y uno visible). Al recibir un valor en el campo 
         honeypot, un valor que no se espera por parte de un usuario normal, la validación será inválida.
        '''
        raise validators.ValidationError(
            'Solo los humanos pueden completar el registro!')


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
            min=4, max=50, message='Mínimo deben ser 4 carácteres para el usuario'),
        # admin_validator -> Validacion por función
        # En este caso no se permite que ningun usuario se registre como 'admin' o 'Admin'
        admin_validator
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
        # validators.length(min=4, message='Mínimo deben ser 4 carácteres para la contraseña'),
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
    # honeypot -> Input antispam
    '''
    El campo será de tipo HiddenField, esto quiere decir que el usuario final no podrá visualizar 
    dicho campo en el navegador, por lo tanto se espera que el campo llegue al servidor sin ningún 
    tipo de valor.
    '''
    honeypot = HiddenField('', [length_honeypot])

    # Validaciones mediante métodos
    # Es necesario definirlos en la misma clase

    # Valida que el usuario no este en la base de datos
    # self -> Pasamos la instancia del modelo
    # username -> El username a validar
    def validate_username(self, username):
        # Con el modelo podemos acceder al método get_by_username
        # En este caso accedemos a 'data' de username
        # Si el username ya se encontro en la base de datos va a regresar True
        if User.get_by_username(username.data):
            # Lanzamos una excepción con raise y mostramos un mensaje de error
            # Igual concatenamos el username
            raise validators.ValidationError(
                f'El usuario "{username.data}" ya se encuentra en uso, por favor ingresa otro')

    # Valida que el email no este en la base de datos
    # self -> Pasamos la instancia del modelo
    # email -> El email a validar
    def validate_email(self, email):
        # Con el modelo podemos acceder al método get_by_email
        # En este caso accedemos a 'email' de username
        # Si el email ya se encontro en la base de datos va a regresar True
        if User.get_by_email(email.data):
            # Lanzamos una excepción con raise y mostramos un mensaje de error
            # Igual concatenamos el email
            raise validators.ValidationError(
                f'El email "{email.data}" ya se encuentra en uso, por favor ingresa otro')

    # Podemos sobreescribir el método por defecto 'validate'
    # Obligatoriament debemos recibir el objeto -> self y retornar un valor booleano
    def validate(self):

        # Hacemos la validación normal del formulario de la clase 'Form'
        # Si no es válida la validación retorna False
        if not Form.validate(self):
            return False

        # A partir de aquí, podemos realizar nuevas validaciones

        # Si la longitud de la contraseña es menor a 4, entonces muestra un mensaje de error
        if len(self.password.data) < 4:
            # Podemos acceder a la propiedad 'errors' que almacena los errores de cada propiedad
            # Y agregar un nuevo error con append()
            self.password.errors.append('La contraseña es demasiada corta')
            return False

        # Si llega a este punto, paso la validación
        return True
