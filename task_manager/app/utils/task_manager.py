import json
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path
from flask import current_app
from app.models.task import Task
from app.models.task_db import TaskDB
from app.database.azure_connection import get_db_session
from config import Config
from sqlalchemy import func
from app.models.user_story_db import UserStory
from sqlalchemy.orm import joinedload
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
                session.close()
        else:
            # Modo JSON (fallback)
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
            try:
                db_task = session.query(TaskDB).filter(TaskDB.id == task_id).first()
                if db_task:
                    return Task.from_dict(db_task.to_dict())
                return None
            finally:
                session.close()
        else:
            # Modo JSON (fallback)
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
                session.close()
        else:
            # Modo JSON (fallback)
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
                session.close()
        else:
            # Modo JSON (fallback)
            raise Exception("Modo JSON no disponible")
    
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
                session.close()
        else:
            # Modo JSON (fallback)
            return None
    
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
                session.close()
        else:
            # Modo JSON (fallback)
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de las tareas.
        
        Returns:
            Dict[str, Any]: Estadísticas de las tareas
        """
        if self.use_database:
            # Usar base de datos
            session = get_db_session()
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
                session.close()
        else:
            # Modo JSON (fallback)
            return {
                'total_tasks': 0,
                'total_tokens': 0,
                'total_costos': 0.0,
                'status_stats': {},
                'priority_stats': {}
            }