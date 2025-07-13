import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from app.database.azure_connection import azure_mysql, get_db_session
from app.models.task_db import TaskDB
from app.models.task import Task
from config import Config
from sqlalchemy import MetaData

logger = logging.getLogger(__name__)

class DataMigrator:
    """Clase para migrar datos del JSON a Azure MySQL"""
    
    def __init__(self):
        self.tasks_file = Config.TASKS_FILE
        self.backup_file = self.tasks_file.parent / 'tasks_backup.json'
    
    def backup_json_data(self) -> bool:
        """Crea un backup del archivo JSON actual"""
        try:
            if self.tasks_file.exists():
                import shutil
                shutil.copy2(self.tasks_file, self.backup_file)
                logger.info(f"✅ Backup creado en: {self.backup_file}")
                return True
            else:
                logger.warning("⚠️ No se encontró archivo JSON para hacer backup")
                return False
        except Exception as e:
            logger.error(f"❌ Error al crear backup: {str(e)}")
            return False
    
    def load_json_tasks(self) -> List[Dict[str, Any]]:
        """Carga las tareas desde el archivo JSON"""
        try:
            if not self.tasks_file.exists():
                logger.warning("⚠️ No se encontró archivo JSON de tareas")
                return []
            
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
                logger.info(f"✅ Cargadas {len(tasks_data)} tareas del JSON")
                return tasks_data
        except Exception as e:
            logger.error(f"❌ Error al cargar JSON: {str(e)}")
            return []
    
    def validate_task_data(self, task_data: Dict[str, Any]) -> bool:
        """Valida que los datos de la tarea sean correctos"""
        required_fields = ['title']
        for field in required_fields:
            if field not in task_data or not task_data[field]:
                logger.warning(f"⚠️ Campo requerido faltante: {field}")
                return False
        return True
    
    def migrate_task_to_db(self, task_data: Dict[str, Any]) -> bool:
        """Migra una tarea individual del JSON a la base de datos"""
        try:
            # Validar datos
            if not self.validate_task_data(task_data):
                return False
            
            # Crear instancia del modelo SQLAlchemy
            task_db = TaskDB.from_dict(task_data)
            
            # Guardar en la base de datos
            session = get_db_session()
            try:
                session.add(task_db)
                session.commit()
                logger.info(f"✅ Tarea migrada: {task_data.get('title', 'Sin título')}")
                return True
            except Exception as e:
                session.rollback()
                logger.error(f"❌ Error al guardar tarea en DB: {str(e)}")
                return False
            finally:
                session.close()
                
        except Exception as e:
            logger.error(f"❌ Error al migrar tarea: {str(e)}")
            return False
    
    def migrate_all_tasks(self) -> Dict[str, Any]:
        """Migra todas las tareas del JSON a Azure MySQL"""
        try:
            logger.info("🚀 Iniciando migración de datos...")
            
            # Crear backup
            backup_success = self.backup_json_data()
            
            # Cargar datos del JSON
            json_tasks = self.load_json_tasks()
            if not json_tasks:
                return {
                    'success': False,
                    'message': 'No se encontraron tareas para migrar',
                    'total_tasks': 0,
                    'migrated_tasks': 0,
                    'failed_tasks': 0,
                    'backup_created': backup_success
                }
            
            # Crear tablas si no existen
            azure_mysql.create_tables()
            
            # Migrar cada tarea
            migrated_count = 0
            failed_count = 0
            
            for task_data in json_tasks:
                if self.migrate_task_to_db(task_data):
                    migrated_count += 1
                else:
                    failed_count += 1
            
            # Resultado final
            result = {
                'success': True,
                'message': f'Migración completada: {migrated_count} tareas migradas, {failed_count} fallidas',
                'total_tasks': len(json_tasks),
                'migrated_tasks': migrated_count,
                'failed_tasks': failed_count,
                'backup_created': backup_success
            }
            
            logger.info(f"✅ Migración completada: {result}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error en migración: {str(e)}")
            return {
                'success': False,
                'message': f'Error en migración: {str(e)}',
                'total_tasks': 0,
                'migrated_tasks': 0,
                'failed_tasks': 0,
                'backup_created': False
            }
    
    def verify_migration(self) -> Dict[str, Any]:
        """Verifica que la migración fue exitosa"""
        try:
            # Contar tareas en JSON
            json_tasks = self.load_json_tasks()
            json_count = len(json_tasks)
            
            # Contar tareas en DB
            session = get_db_session()
            try:
                db_count = session.query(TaskDB).count()
                logger.info(f"📊 Verificación: {json_count} tareas en JSON, {db_count} tareas en DB")
                
                return {
                    'success': True,
                    'json_count': json_count,
                    'db_count': db_count,
                    'match': json_count == db_count,
                    'message': f'Verificación completada: JSON={json_count}, DB={db_count}'
                }
            finally:
                session.close()
                
        except Exception as e:
            logger.error(f"❌ Error en verificación: {str(e)}")
            return {
                'success': False,
                'message': f'Error en verificación: {str(e)}',
                'json_count': 0,
                'db_count': 0,
                'match': False
            }
    
    def rollback_migration(self) -> bool:
        """Hace rollback de la migración (elimina todas las tareas de la DB)"""
        try:
            logger.warning("⚠️ Iniciando rollback de migración...")
            
            session = get_db_session()
            try:
                # Eliminar todas las tareas
                deleted_count = session.query(TaskDB).delete()
                session.commit()
                logger.info(f"✅ Rollback completado: {deleted_count} tareas eliminadas")
                return True
            except Exception as e:
                session.rollback()
                logger.error(f"❌ Error en rollback: {str(e)}")
                return False
            finally:
                session.close()
                
        except Exception as e:
            logger.error(f"❌ Error en rollback: {str(e)}")
            return False

def run_migration():
    """Función principal para ejecutar la migración"""
    migrator = DataMigrator()
    
    print("🚀 Iniciando migración de datos del JSON a Azure MySQL...")
    
    # Ejecutar migración
    result = migrator.migrate_all_tasks()
    
    if result['success']:
        print(f"✅ {result['message']}")
        
        # Verificar migración
        verification = migrator.verify_migration()
        if verification['success']:
            print(f"✅ {verification['message']}")
            if verification['match']:
                print("🎉 ¡Migración exitosa y verificada!")
            else:
                print("⚠️ Migración completada pero hay discrepancias en el conteo")
        else:
            print(f"❌ Error en verificación: {verification['message']}")
    else:
        print(f"❌ {result['message']}")
    
    return result

if __name__ == "__main__":
    session = get_db_session()
    metadata = MetaData()
    metadata.reflect(bind=session.bind)
    print("Borrando todas las tablas...")
    metadata.drop_all(bind=session.bind)
    print("¡Base de datos borrada correctamente!") 