#!/usr/bin/env python3
"""
Script de diagnóstico para la conexión a Azure MySQL
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Archivo .env cargado desde: {env_path}")
else:
    print(f"❌ Archivo .env no encontrado en: {env_path}")
    sys.exit(1)

def test_env_variables():
    """Prueba que las variables de entorno estén configuradas"""
    print("\n🔍 Verificando variables de entorno...")
    
    # Variables requeridas
    required_vars = [
        'AZURE_MYSQL_CONNECTION_STRING',
        'AZURE_MYSQL_SSL_CA',
        'AZURE_MYSQL_SSL_VERIFY'
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mostrar solo los primeros 50 caracteres para seguridad
            display_value = value[:50] + "..." if len(value) > 50 else value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: NO CONFIGURADA")
            return False
    
    return True

def test_ssl_certificate():
    """Prueba que el certificado SSL exista"""
    print("\n🔍 Verificando certificado SSL...")
    
    ssl_ca_path = os.getenv('AZURE_MYSQL_SSL_CA')
    if not ssl_ca_path:
        print("❌ AZURE_MYSQL_SSL_CA no está configurada")
        return False
    
    ssl_path = Path(ssl_ca_path)
    if ssl_path.exists():
        print(f"✅ Certificado SSL encontrado: {ssl_path}")
        print(f"   Tamaño: {ssl_path.stat().st_size} bytes")
        return True
    else:
        print(f"❌ Certificado SSL no encontrado: {ssl_path}")
        return False

def test_mysql_connection():
    """Prueba la conexión directa a MySQL"""
    print("\n🔍 Probando conexión directa a MySQL...")
    
    try:
        import mysql.connector
        from sqlalchemy import create_engine, text
        
        connection_string = os.getenv('AZURE_MYSQL_CONNECTION_STRING')
        ssl_ca = os.getenv('AZURE_MYSQL_SSL_CA')
        ssl_verify = str(os.getenv('AZURE_MYSQL_SSL_VERIFY', 'true')).lower() == 'true'
        
        print(f"📋 Connection string: {connection_string[:50]}...")
        print(f"📋 SSL CA: {ssl_ca}")
        print(f"📋 SSL Verify: {ssl_verify}")
        
        # Configurar SSL
        ssl_config = {}
        if ssl_ca:
            ssl_config = {
                'ssl': {
                    'ca': ssl_ca,
                    'verify_cert': ssl_verify
                }
            }
        
        # Crear engine
        print("🔄 Creando engine de SQLAlchemy...")
        engine = create_engine(
            connection_string,
            pool_size=5,
            pool_recycle=3600,
            pool_pre_ping=True,
            connect_args=ssl_config
        )
        
        # Probar conexión
        print("🔄 Probando conexión...")
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            print(f"✅ Conexión exitosa! Resultado: {row[0]}")
            return True
            
    except Exception as e:
        print(f"❌ Error en la conexión: {str(e)}")
        print(f"   Tipo de error: {type(e).__name__}")
        return False

def test_azure_connection_class():
    """Prueba la clase AzureMySQLConnection"""
    print("\n🔍 Probando clase AzureMySQLConnection...")
    
    try:
        from app.database.azure_connection import AzureMySQLConnection
        
        print("🔄 Creando instancia de AzureMySQLConnection...")
        azure_mysql = AzureMySQLConnection()
        
        if azure_mysql.engine is None:
            print("❌ Engine no se creó correctamente")
            return False
        
        print("✅ Engine creado correctamente")
        
        # Probar test_connection
        print("🔄 Probando test_connection...")
        if azure_mysql.test_connection():
            print("✅ test_connection exitoso")
            return True
        else:
            print("❌ test_connection falló")
            return False
            
    except Exception as e:
        print(f"❌ Error en AzureMySQLConnection: {str(e)}")
        print(f"   Tipo de error: {type(e).__name__}")
        return False

def main():
    """Función principal de diagnóstico"""
    print("🚀 Iniciando diagnóstico de conexión a Azure MySQL...")
    print("=" * 60)
    
    # Paso 1: Verificar variables de entorno
    if not test_env_variables():
        print("\n❌ Variables de entorno incompletas")
        return
    
    # Paso 2: Verificar certificado SSL
    if not test_ssl_certificate():
        print("\n❌ Problema con el certificado SSL")
        return
    
    # Paso 3: Probar conexión directa
    if not test_mysql_connection():
        print("\n❌ Problema con la conexión directa a MySQL")
        return
    
    # Paso 4: Probar clase AzureMySQLConnection
    if not test_azure_connection_class():
        print("\n❌ Problema con la clase AzureMySQLConnection")
        return
    
    print("\n🎉 ¡Diagnóstico completado! Todos los tests pasaron.")
    print("La conexión a Azure MySQL debería funcionar correctamente.")

if __name__ == "__main__":
    main() 