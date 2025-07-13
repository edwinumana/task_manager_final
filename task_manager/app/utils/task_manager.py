import logging
from typing import List, Dict, Any, Optional
from app.models.task_db import TaskDB
from app.models.task import Task
from app.database.azure_connection import get_db_session
from sqlalchemy.orm import joinedload
from sqlalchemy import func
import json
from pathlib import Path
from datetime import datetime

def truncate_text(text: str, max_words: int = 30) -> str:
    """
    Trunca un texto a un número máximo de palabras.
    
    Args:
        text: Texto a truncar
        max_words: Número máximo de palabras
        
    Returns:
        str: Texto truncado
    """
    if not text:
        return ""
    
    words = text.split()
    if len(words) <= max_words:
        return text
    
    return " ".join(words[:max_words]) + "..."

class TaskManager:
    """
    Clase para gestionar las tareas usando Azure MySQL con SQLAlchemy.
    Mantiene compatibilidad con el modelo Task existente.
    """
    
    def __init__(self, use_database: bool = True):
        """
        Inicializa el gestor de tareas.
        Usa Azure MySQL como base de datos principal.
        """
        self.use_database = use_database
    

    
    def get_next_id(self) -> int:
        """
        Obtiene el siguiente ID disponible para una nueva tarea.
        
        Returns:
            int: Siguiente ID disponible
        """
        if self.use_database:
            # Usar base de datos
            session = get_db_session()
            try:
                max_id = session.query(TaskDB.id).order_by(TaskDB.id.desc()).first()
                return (max_id[0] + 1) if max_id else 1
            finally:
                if session is not None:
                    session.close()
        else:
            # Modo JSON (fallback)
            return 1
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las tareas con datos del user story asociado y fecha formateada.
        """
        if self.use_database:
            session = get_db_session()
            if session is None:
                # No hay conexión a base de datos, usar modo JSON
                print("⚠️ No hay conexión a base de datos - usando modo JSON")
                return self._get_tasks_from_json()
            try:
                db_tasks = (
                    session.query(TaskDB)
                    .options(joinedload(TaskDB.user_story))
                    .order_by(TaskDB.created_at.desc())
                    .all()
                )
                tasks = []
                for task in db_tasks:
                    task_dict = task.to_dict()
                    # Formatear fecha de creación
                    if task.created_at:
                        task_dict['created_at'] = task.created_at.isoformat()
                    else:
                        task_dict['created_at'] = ''
                    
                    # Truncar descripción de la tarea
                    task_dict['description_truncated'] = truncate_text(task_dict.get('description', ''), 30)
                    
                    # Añadir datos del user story asociado
                    user_story = getattr(task, 'user_story', None)
                    if user_story:
                        task_dict['user_story_project'] = user_story.project
                        task_dict['user_story_role'] = user_story.role
                        task_dict['user_story_goal'] = user_story.goal
                        task_dict['user_story_reason'] = user_story.reason
                        task_dict['user_story_priority'] = user_story.priority.value if user_story.priority else ''
                        task_dict['user_story_description'] = user_story.description
                        task_dict['user_story_description_truncated'] = truncate_text(user_story.description, 30)
                    else:
                        task_dict['user_story_project'] = ''
                        task_dict['user_story_role'] = ''
                        task_dict['user_story_goal'] = ''
                        task_dict['user_story_reason'] = ''
                        task_dict['user_story_priority'] = ''
                        task_dict['user_story_description'] = ''
                        task_dict['user_story_description_truncated'] = ''
                    tasks.append(task_dict)
                return tasks
            finally:
                if session is not None:
                    session.close()
        else:
            # Modo JSON (fallback)
            return self._get_tasks_from_json()

    def _get_tasks_from_json(self) -> List[Dict[str, Any]]:
        """Obtiene tareas desde archivo JSON"""
        try:
            json_file = Path(__file__).parent.parent.parent / 'data' / 'tasks.json'
            if not json_file.exists():
                return []
            
            with open(json_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
            
            # Convertir a formato esperado
            tasks = []
            for task_data in tasks_data:
                task_dict = {
                    'id': task_data.get('id'),
                    'title': task_data.get('title', ''),
                    'description': task_data.get('description', ''),
                    'description_truncated': truncate_text(task_data.get('description', ''), 30),
                    'priority': task_data.get('priority', 'media'),
                    'status': task_data.get('status', 'pendiente'),
                    'effort': task_data.get('effort', 0),
                    'assigned_to': task_data.get('assigned_to', ''),
                    'assigned_role': task_data.get('assigned_role', ''),
                    'category': task_data.get('category', 'OTRO'),
                    'risk_analysis': task_data.get('risk_analysis', ''),
                    'mitigation_plan': task_data.get('mitigation_plan', ''),
                    'tokens_gastados': task_data.get('tokens_gastados', 0),
                    'costos': task_data.get('costos', 0.0),
                    'created_at': task_data.get('created_at', ''),
                    'updated_at': task_data.get('updated_at', ''),
                    'user_story_id': task_data.get('user_story_id'),
                    'user_story_project': '',
                    'user_story_role': '',
                    'user_story_goal': '',
                    'user_story_reason': '',
                    'user_story_priority': '',
                    'user_story_description': '',
                    'user_story_description_truncated': ''
                }
                tasks.append(task_dict)
            
            return tasks
        except Exception as e:
            print(f"Error cargando tareas desde JSON: {e}")
            return []

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Obtiene una tarea por su ID.
        
        Args:
            task_id: ID de la tarea a buscar
            
        Returns:
            Optional[Task]: La tarea encontrada o None si no existe
        """
        if self.use_database:
            # Usar base de datos
            session = get_db_session()
            if session is None:
                # No hay conexión a base de datos, usar modo JSON
                return self._get_task_from_json(task_id)
            try:
                db_task = session.query(TaskDB).filter(TaskDB.id == task_id).first()
                if db_task:
                    return Task.from_dict(db_task.to_dict())
                return None
            finally:
                if session is not None:
                    session.close()
        else:
            # Modo JSON (fallback)
            return self._get_task_from_json(task_id)

    def _get_task_from_json(self, task_id: int) -> Optional[Task]:
        """Obtiene una tarea desde archivo JSON"""
        try:
            json_file = Path(__file__).parent.parent.parent / 'data' / 'tasks.json'
            if not json_file.exists():
                return None
            
            with open(json_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
            
            for task_data in tasks_data:
                if task_data.get('id') == task_id:
                    return Task.from_dict(task_data)
            
            return None
        except Exception as e:
            print(f"Error obteniendo tarea desde JSON: {e}")
            return None
    
    def get_task_with_user_story(self, task_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene una tarea por su ID con información de User Story.
        
        Args:
            task_id: ID de la tarea a buscar
            
        Returns:
            Optional[Dict[str, Any]]: La tarea con datos de User Story o None si no existe
        """
        if self.use_database:
            # Usar base de datos
            session = get_db_session()
            if session is None:
                # No hay conexión a base de datos, usar modo JSON
                return self._get_task_with_user_story_from_json(task_id)
            try:
                db_task = (
                    session.query(TaskDB)
                    .options(joinedload(TaskDB.user_story))
                    .filter(TaskDB.id == task_id)
                    .first()
                )
                if db_task:
                    task_dict = db_task.to_dict()
                    # Formatear fecha de creación
                    if db_task.created_at:
                        task_dict['created_at'] = db_task.created_at.isoformat()
                    else:
                        task_dict['created_at'] = ''
                    
                    # Formatear fecha de actualización
                    if db_task.updated_at:
                        task_dict['updated_at'] = db_task.updated_at.isoformat()
                    else:
                        task_dict['updated_at'] = ''
                    
                    # Añadir datos del user story asociado
                    user_story = getattr(db_task, 'user_story', None)
                    if user_story:
                        task_dict['user_story_project'] = user_story.project
                        task_dict['user_story_role'] = user_story.role
                        task_dict['user_story_goal'] = user_story.goal
                        task_dict['user_story_reason'] = user_story.reason
                        task_dict['user_story_priority'] = user_story.priority.value if user_story.priority else ''
                        task_dict['user_story_description'] = user_story.description
                    else:
                        task_dict['user_story_project'] = ''
                        task_dict['user_story_role'] = ''
                        task_dict['user_story_goal'] = ''
                        task_dict['user_story_reason'] = ''
                        task_dict['user_story_priority'] = ''
                        task_dict['user_story_description'] = ''
                    
                    return task_dict
                return None
            finally:
                if session is not None:
                    session.close()
        else:
            # Modo JSON (fallback)
            return self._get_task_with_user_story_from_json(task_id)

    def _get_task_with_user_story_from_json(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene una tarea con user story desde archivo JSON"""
        try:
            json_file = Path(__file__).parent.parent.parent / 'data' / 'tasks.json'
            if not json_file.exists():
                return None
            
            with open(json_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
            
            for task_data in tasks_data:
                if task_data.get('id') == task_id:
                    # Convertir a formato esperado
                    task_dict = {
                        'id': task_data.get('id'),
                        'title': task_data.get('title', ''),
                        'description': task_data.get('description', ''),
                        'priority': task_data.get('priority', 'media'),
                        'status': task_data.get('status', 'pendiente'),
                        'effort': task_data.get('effort', 0),
                        'assigned_to': task_data.get('assigned_to', ''),
                        'assigned_role': task_data.get('assigned_role', ''),
                        'category': task_data.get('category', 'OTRO'),
                        'risk_analysis': task_data.get('risk_analysis', ''),
                        'mitigation_plan': task_data.get('mitigation_plan', ''),
                        'tokens_gastados': task_data.get('tokens_gastados', 0),
                        'costos': task_data.get('costos', 0.0),
                        'created_at': task_data.get('created_at', ''),
                        'updated_at': task_data.get('updated_at', ''),
                        'user_story_id': task_data.get('user_story_id'),
                        'user_story_project': '',
                        'user_story_role': '',
                        'user_story_goal': '',
                        'user_story_reason': '',
                        'user_story_priority': '',
                        'user_story_description': ''
                    }
                    return task_dict
            
            return None
        except Exception as e:
            print(f"Error obteniendo tarea con user story desde JSON: {e}")
            return None
    
    def create_task(self, task_data: dict) -> Task:
        """
        Crea una nueva tarea.
        
        Args:
            task_data: Diccionario con los datos de la tarea
            
        Returns:
            Task: La tarea creada
        """
        if self.use_database:
            # Usar base de datos
            session = get_db_session()
            if session is None:
                # No hay conexión a base de datos, usar modo JSON
                return self._create_task_in_json(task_data)
            try:
                # Crear instancia del modelo SQLAlchemy
                task_db = TaskDB.from_dict(task_data)
                session.add(task_db)
                session.commit()
                session.refresh(task_db)
                
                # Convertir a modelo Task para compatibilidad
                return Task.from_dict(task_db.to_dict())
            except Exception as e:
                session.rollback()
                logging.error(f"Error al crear tarea en DB: {str(e)}")
                raise
            finally:
                if session is not None:
                    session.close()
        else:
            # Modo JSON (fallback)
            return self._create_task_in_json(task_data)

    def _create_task_in_json(self, task_data: dict) -> Task:
        """Crea una tarea en archivo JSON"""
        try:
            json_file = Path(__file__).parent.parent.parent / 'data' / 'tasks.json'
            json_file.parent.mkdir(exist_ok=True)
            
            # Cargar tareas existentes
            if json_file.exists():
                with open(json_file, 'r', encoding='utf-8') as f:
                    tasks_data = json.load(f)
            else:
                tasks_data = []
            
            # Generar ID único
            max_id = max([item.get('id', 0) for item in tasks_data]) if tasks_data else 0
            task_data['id'] = max_id + 1
            
            # Agregar timestamps
            now = datetime.now()
            task_data['created_at'] = now.isoformat()
            task_data['updated_at'] = now.isoformat()
            
            # Guardar en JSON
            tasks_data.append(task_data)
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, indent=2, ensure_ascii=False, default=str)
            
            return Task.from_dict(task_data)
        except Exception as e:
            print(f"Error creando tarea en JSON: {e}")
            raise
    
    def update_task(self, task_id: int, task_data: dict) -> Optional[Task]:
        """
        Actualiza una tarea existente.
        
        Args:
            task_id: ID de la tarea a actualizar
            task_data: Diccionario con los nuevos datos
            
        Returns:
            Optional[Task]: La tarea actualizada o None si no existe
        """
        if self.use_database:
            # Usar base de datos
            session = get_db_session()
            if session is None:
                # No hay conexión a base de datos, usar modo JSON
                return self._update_task_in_json(task_id, task_data)
            try:
                db_task = session.query(TaskDB).filter(TaskDB.id == task_id).first()
                if not db_task:
                    return None
                
                # Actualizar campos
                for key, value in task_data.items():
                    if hasattr(db_task, key):
                        setattr(db_task, key, value)
                
                session.commit()
                session.refresh(db_task)
                
                # Convertir a modelo Task para compatibilidad
                return Task.from_dict(db_task.to_dict())
            except Exception as e:
                session.rollback()
                logging.error(f"Error al actualizar tarea en DB: {str(e)}")
                raise
            finally:
                if session is not None:
                    session.close()
        else:
            # Modo JSON (fallback)
            return self._update_task_in_json(task_id, task_data)

    def _update_task_in_json(self, task_id: int, task_data: dict) -> Optional[Task]:
        """Actualiza una tarea en archivo JSON"""
        try:
            json_file = Path(__file__).parent.parent.parent / 'data' / 'tasks.json'
            if not json_file.exists():
                return None
            
            # Cargar tareas existentes
            with open(json_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
            
            # Buscar y actualizar la tarea
            for i, task in enumerate(tasks_data):
                if task.get('id') == task_id:
                    # Actualizar campos
                    for key, value in task_data.items():
                        if key in task:
                            task[key] = value
                    
                    # Actualizar timestamp
                    task['updated_at'] = datetime.now().isoformat()
                    
                    # Guardar en JSON
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(tasks_data, f, indent=2, ensure_ascii=False, default=str)
                    
                    return Task.from_dict(task)
            
            return None
        except Exception as e:
            print(f"Error actualizando tarea en JSON: {e}")
            return None

    def _delete_task_in_json(self, task_id: int) -> bool:
        """Elimina una tarea desde archivo JSON"""
        try:
            json_file = Path(__file__).parent.parent.parent / 'data' / 'tasks.json'
            if not json_file.exists():
                return False
            
            # Cargar tareas existentes
            with open(json_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
            
            # Buscar y eliminar la tarea
            for i, task in enumerate(tasks_data):
                if task.get('id') == task_id:
                    del tasks_data[i]
                    
                    # Guardar en JSON
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(tasks_data, f, indent=2, ensure_ascii=False, default=str)
                    
                    return True
            
            return False
        except Exception as e:
            print(f"Error eliminando tarea en JSON: {e}")
            return False

    def delete_task(self, task_id: int) -> bool:
        """
        Elimina una tarea.
        
        Args:
            task_id: ID de la tarea a eliminar
            
        Returns:
            bool: True si se eliminó la tarea, False si no existe
        """
        if self.use_database:
            # Usar base de datos
            session = get_db_session()
            if session is None:
                # No hay conexión a base de datos, usar modo JSON
                return self._delete_task_in_json(task_id)
            try:
                db_task = session.query(TaskDB).filter(TaskDB.id == task_id).first()
                if not db_task:
                    return False
                
                session.delete(db_task)
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                logging.error(f"Error al eliminar tarea en DB: {str(e)}")
                return False
            finally:
                if session is not None:
                    session.close()
        else:
            # Modo JSON (fallback)
            return self._delete_task_in_json(task_id)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de las tareas.
        
        Returns:
            Dict[str, Any]: Estadísticas de las tareas
        """
        if self.use_database:
            # Usar base de datos
            session = get_db_session()
            if session is None:
                # No hay conexión a base de datos, usar modo JSON
                return self._get_stats_from_json()
            try:
                total_tasks = session.query(TaskDB).count()
                total_tokens = session.query(TaskDB.tokens_gastados).with_entities(
                    func.sum(TaskDB.tokens_gastados)
                ).scalar() or 0
                total_costos = session.query(TaskDB.costos).with_entities(
                    func.sum(TaskDB.costos)
                ).scalar() or 0.0
                
                # Estadísticas por estado
                status_stats = {}
                for status in ['pendiente', 'en_progreso', 'en_revision', 'completada']:
                    count = session.query(TaskDB).filter(TaskDB.status == status).count()
                    status_stats[status] = count
                
                # Estadísticas por prioridad
                priority_stats = {}
                for priority in ['baja', 'media', 'alta', 'bloqueante']:
                    count = session.query(TaskDB).filter(TaskDB.priority == priority).count()
                    priority_stats[priority] = count
                
                return {
                    'total_tasks': total_tasks,
                    'total_tokens': total_tokens,
                    'total_costos': float(total_costos),
                    'status_stats': status_stats,
                    'priority_stats': priority_stats
                }
            finally:
                if session is not None:
                    session.close()
        else:
            # Modo JSON (fallback)
            return self._get_stats_from_json()

    def _get_stats_from_json(self) -> Dict[str, Any]:
        """Obtiene estadísticas desde archivo JSON"""
        try:
            json_file = Path(__file__).parent.parent.parent / 'data' / 'tasks.json'
            if not json_file.exists():
                return {
                    'total_tasks': 0,
                    'total_tokens': 0,
                    'total_costos': 0.0,
                    'status_stats': {},
                    'priority_stats': {}
                }
            
            with open(json_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
            
            total_tasks = len(tasks_data)
            total_tokens = sum(task.get('tokens_gastados', 0) for task in tasks_data)
            total_costos = sum(task.get('costos', 0.0) for task in tasks_data)
            
            # Estadísticas por estado
            status_stats = {}
            for status in ['pendiente', 'en_progreso', 'en_revision', 'completada']:
                count = sum(1 for task in tasks_data if task.get('status') == status)
                status_stats[status] = count
            
            # Estadísticas por prioridad
            priority_stats = {}
            for priority in ['baja', 'media', 'alta', 'bloqueante']:
                count = sum(1 for task in tasks_data if task.get('priority') == priority)
                priority_stats[priority] = count
            
            return {
                'total_tasks': total_tasks,
                'total_tokens': total_tokens,
                'total_costos': float(total_costos),
                'status_stats': status_stats,
                'priority_stats': priority_stats
            }
        except Exception as e:
            print(f"Error obteniendo estadísticas desde JSON: {e}")
            return {
                'total_tasks': 0,
                'total_tokens': 0,
                'total_costos': 0.0,
                'status_stats': {},
                'priority_stats': {}
            }