# Realizamos la configuración del entorno
class Config:
    pass


# Primero creamos una clase para la configuración de desarrollo
class DevelopmentConfig(Config):
    # Colocamos DEBUG en True para el auto reload y demás ayuda para desarrollar el proyecto
    DEBUG = True


# Creamos un diccionario que contenga dicha configuración
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
