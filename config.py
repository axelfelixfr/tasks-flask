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


# Creamos un diccionario que contenga dicha configuración
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
