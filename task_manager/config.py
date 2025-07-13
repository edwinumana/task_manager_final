import os
from pathlib import Path

class Config:
    # Directorio base de la aplicación
    BASE_DIR = Path(__file__).resolve().parent
    
    # Ruta al archivo JSON de tareas (mantener para migración)
    TASKS_FILE = BASE_DIR / 'data' / 'tasks.json'
    
    # Configuración de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    DEBUG = True
    
    # Configuración de Azure MySQL
    AZURE_MYSQL_CONNECTION_STRING = os.environ.get('AZURE_MYSQL_CONNECTION_STRING')
    AZURE_MYSQL_SSL_CA = os.environ.get('AZURE_MYSQL_SSL_CA')
    AZURE_MYSQL_SSL_VERIFY = os.environ.get('AZURE_MYSQL_SSL_VERIFY', 'true').lower() == 'true'
    
    # Configuración de SQLAlchemy
    SQLALCHEMY_DATABASE_URI = AZURE_MYSQL_CONNECTION_STRING
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'connect_args': {
            'ssl': {
                'ca': AZURE_MYSQL_SSL_CA,
                'verify_cert': AZURE_MYSQL_SSL_VERIFY
            } if AZURE_MYSQL_SSL_CA else {}
        }
    }

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}