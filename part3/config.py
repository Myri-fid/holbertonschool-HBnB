import os

class Config:
    SECRET_KEY = 'votre_cle_secrete'
    DEBUG = True
    #SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    #DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
