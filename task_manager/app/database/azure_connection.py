import ssl
import mysql.connector as con
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import current_app
import os
from config import Config

Base = declarative_base()

class AzureMySQLConnection:
    """Clase para manejar la conexión a Azure MySQL con SSL"""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._setup_connection()
    
    def _setup_connection(self):
        """Configura la conexión a Azure MySQL con SSL"""
        try:
            # Obtener configuración desde variables de entorno
            connection_string = os.getenv('AZURE_MYSQL_CONNECTION_STRING')
            ssl_ca = os.getenv('AZURE_MYSQL_SSL_CA')
            ssl_verify = os.getenv('AZURE_MYSQL_SSL_VERIFY', 'true').lower() == 'true'
            
            if not connection_string:
                print("⚠️ AZURE_MYSQL_CONNECTION_STRING no está configurada. Modo sin base de datos.")
                self.engine = None
                self.SessionLocal = None
                return
            
            # Configurar SSL para Azure MySQL
            ssl_config = {}
            if ssl_ca:
                ssl_config = {
                    'ssl': {
                        'ca': ssl_ca,
                        'verify_cert': ssl_verify
                    }
                }
            
            # Crear engine de SQLAlchemy con configuración SSL
            self.engine = create_engine(
                connection_string,
                pool_size=10,
                pool_recycle=3600,
                pool_pre_ping=True,
                connect_args=ssl_config
            )
            
            # Crear sesión local
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            print("✅ Conexión a Azure MySQL configurada exitosamente")
            
        except Exception as e:
            print(f"❌ Error al configurar conexión a Azure MySQL: {str(e)}")
            raise
    
    def get_session(self):
        """Obtiene una sesión de base de datos"""
        if not self.SessionLocal:
            self._setup_connection()
        if not self.SessionLocal:
            return None
        return self.SessionLocal()
    
    def create_tables(self):
        """Crea todas las tablas definidas en los modelos"""
        if not self.engine:
            print("⚠️ No hay conexión a base de datos disponible")
            return False
        try:
            Base.metadata.create_all(bind=self.engine)
            print("✅ Tablas creadas exitosamente")
            return True
        except Exception as e:
            print(f"❌ Error al crear tablas: {str(e)}")
            return False
    
    def test_connection(self):
        """Prueba la conexión a la base de datos"""
        if not self.engine:
            print("⚠️ No hay conexión a base de datos disponible")
            return False
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                print("✅ Conexión a Azure MySQL probada exitosamente")
                return True
        except Exception as e:
            print(f"❌ Error al probar conexión: {str(e)}")
            return False

# Instancia global de la conexión (inicialización segura)
try:
    azure_mysql = AzureMySQLConnection()
except Exception as e:
    print(f"⚠️ Error al inicializar conexión a Azure MySQL: {str(e)}")
    azure_mysql = None

def get_db_session():
    """Función helper para obtener sesión de base de datos"""
    if not azure_mysql:
        return None
    return azure_mysql.get_session() 