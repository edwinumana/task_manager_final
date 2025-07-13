import logging
from app.database.azure_connection import azure_mysql, Base
from app.models.task_db import TaskDB
from app.models.user_story_db import UserStory

logger = logging.getLogger(__name__)

def init_database():
    """Inicializa la base de datos creando las tablas"""
    try:
        logger.info("🚀 Inicializando base de datos...")
        
        # Crear todas las tablas
        azure_mysql.create_tables()
        
        logger.info("✅ Base de datos inicializada exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error al inicializar base de datos: {str(e)}")
        return False

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    try:
        logger.info("🔍 Probando conexión a Azure MySQL...")
        
        # Probar conexión
        if azure_mysql.test_connection():
            logger.info("✅ Conexión a Azure MySQL exitosa")
            return True
        else:
            logger.error("❌ Error en la conexión a Azure MySQL")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error al probar conexión: {str(e)}")
        return False

def create_sample_data():
    """Crea datos de ejemplo en la base de datos"""
    try:
        logger.info("📝 Creando datos de ejemplo...")
        
        from app.database.azure_connection import get_db_session
        
        session = get_db_session()
        
        # Verificar si ya hay datos
        existing_count = session.query(TaskDB).count()
        if existing_count > 0:
            logger.info(f"⚠️ Ya existen {existing_count} tareas en la base de datos")
            session.close()
            return True
        
        # Crear tarea de ejemplo
        sample_task = TaskDB(
            title="Tarea de ejemplo - Migración a Azure MySQL",
            description="Esta es una tarea de ejemplo creada durante la migración a Azure MySQL. Sirve para verificar que la base de datos funciona correctamente.",
            priority="media",
            effort=4,
            status="pendiente",
            assigned_to="Sistema",
            assigned_role="Administrador",
            category="testing",
            risk_analysis="Tarea de prueba sin riesgos significativos.",
            mitigation_plan="No se requiere plan de mitigación para esta tarea de prueba.",
            tokens_gastados=0,
            costos=0.0
        )
        
        session.add(sample_task)
        session.commit()
        session.close()
        
        logger.info("✅ Datos de ejemplo creados exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error al crear datos de ejemplo: {str(e)}")
        return False

def run_database_setup():
    """Ejecuta la configuración completa de la base de datos"""
    print("🚀 Configurando base de datos Azure MySQL...")
    
    # Probar conexión
    if not test_database_connection():
        print("❌ No se pudo conectar a Azure MySQL")
        return False
    
    # Inicializar base de datos
    if not init_database():
        print("❌ No se pudo inicializar la base de datos")
        return False
    
    # Crear datos de ejemplo
    if not create_sample_data():
        print("❌ No se pudieron crear datos de ejemplo")
        return False
    
    print("🎉 Configuración de base de datos completada exitosamente")
    return True

if __name__ == "__main__":
    run_database_setup() 