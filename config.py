# decouple -> Para acceder a variables de entorno
from decouple import config


# Realizamos la configuración del entorno
class Config:
    SECRET_KEY = 'STBE-5DDS-C2GG-LDNH-N37K'


# Primero creamos una clase para la configuración de desarrollo
class DevelopmentConfig(Config):
    # Colocamos DEBUG en True para el auto reload y demás ayuda para desarrollar el proyecto
    DEBUG = True

    # Para realizar la conexión a la base de datos con SQLAlchemy es necesario armar la URL
    # La url deben ser así: 'manejador://<usuario>:<password>@<hostname>/<base_de_datos>'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/tasks_flask'

    # Modificaciones en False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Constantes para enviar los correos
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # config -> Podemos acceder a las variables de entorno a través de su nombre
    MAIL_USERNAME = config('MAIL_USERNAME')
    MAIL_PASSWORD = config('MAIL_PASSWORD')


# Creamos un diccionario que contenga dicha configuración
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
