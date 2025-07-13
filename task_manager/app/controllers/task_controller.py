from flask import current_app, jsonify, request, redirect, url_for
from typing import Tuple, Dict, Any
from app.utils.task_manager import TaskManager
from app.models.task import Task
from app.models.enums import TaskCategory
from app.services.ai_service import AIService
from app.models.task_db import TaskDB
from app.database.azure_connection import get_db_session
import logging

logger = logging.getLogger(__name__)

class TaskController:
    """Controlador para operaciones de tareas"""
    
    def __init__(self):
        """Inicializa el controlador con una instancia de TaskManager"""
        self.task_manager = TaskManager()
    
    def get_all_tasks(self) -> Tuple[Dict[str, Any], int]:
        """Obtiene todas las tareas con información de historia de usuario"""
        try:
            # Usar TaskManager actualizado que ya incluye información de User Story
            tasks = self.task_manager.get_all_tasks()
            
            # Convertir categorías a nombres de visualización
            category_display_names = TaskCategory.get_display_names()
            tasks_with_display_names = []
            
            for task_dict in tasks:
                # Convertir categoría a nombre de visualización
                task_dict['category'] = category_display_names.get(task_dict['category'], 'Otro')
                
                # Asegurar que el campo user_story_project tenga un valor por defecto
                if not task_dict.get('user_story_project'):
                    task_dict['user_story_project'] = 'Sin proyecto asignado'
                
                tasks_with_display_names.append(task_dict)
            
            return {
                'success': True,
                'tasks': tasks_with_display_names,
                'total': len(tasks_with_display_names)
            }, 200
        
        except Exception as e:
            return {
                'success': False,
                'error': 'Error interno del servidor',
                'message': str(e)
            }, 500
    
    def get_task_by_id(self, task_id: int) -> Tuple[Dict[str, Any], int]:
        """Obtiene una tarea específica por ID"""
        try:
            task = self.task_manager.get_task(task_id)
            
            if not task:
                return {
                    'success': False,
                    'error': 'Tarea no encontrada'
                }, 404
            
            task_dict = task.to_dict()
            # Convertir categoría a nombre de visualización
            category_display_names = TaskCategory.get_display_names()
            task_dict['category'] = category_display_names.get(task_dict['category'], 'Otro')
            
            return {
                'success': True,
                'data': task_dict
            }, 200
        
        except Exception as e:
            return {
                'success': False,
                'error': 'Error interno del servidor',
                'message': str(e)
            }, 500
    
    def get_task_with_user_story(self, task_id: int) -> Tuple[Dict[str, Any], int]:
        """Obtiene una tarea específica por ID con información de User Story"""
        try:
            task_data = self.task_manager.get_task_with_user_story(task_id)
            
            if not task_data:
                return {
                    'success': False,
                    'error': 'Tarea no encontrada'
                }, 404
            
            return {
                'success': True,
                'data': task_data
            }, 200
        
        except Exception as e:
            return {
                'success': False,
                'error': 'Error interno del servidor',
                'message': str(e)
            }, 500
    
    def create_task(self) -> Tuple[Dict[str, Any], int]:
        """Crea una nueva tarea"""
        try:
            data = request.get_json()
            
            if not data:
                return {
                    'success': False,
                    'error': 'No se proporcionaron datos'
                }, 400
            
            # Validaciones básicas
            if not data.get('title'):
                return {
                    'success': False,
                    'error': 'El título es requerido'
                }, 400
            
            # Establecer valores por defecto
            if not data.get('status'):
                data['status'] = 'pendiente'
            if not data.get('priority'):
                data['priority'] = 'media'
            if not data.get('assigned_to'):
                data['assigned_to'] = 'No asignado'
            
            # Validar prioridad
            if data.get('priority') and data['priority'] not in Task.VALID_PRIORITIES:
                data['priority'] = 'media'  # Valor por defecto si es inválido
            
            # Validar estado
            if data.get('status') and data['status'] not in Task.VALID_STATUSES:
                data['status'] = 'pendiente'  # Valor por defecto si es inválido
            
            # Manejar el campo effort
            if not data.get('effort') or data['effort'] == '':
                data['effort'] = 0
            
            new_task = self.task_manager.create_task(data)
            
            if not new_task:
                return {
                    'success': False,
                    'error': 'Error al crear la tarea'
                }, 500
            
            task_dict = new_task.to_dict()
            # Convertir categoría a nombre de visualización
            category_display_names = TaskCategory.get_display_names()
            task_dict['category'] = category_display_names.get(task_dict['category'], 'Otro')
            
            return {
                'success': True,
                'data': task_dict,
                'message': 'Tarea creada exitosamente'
            }, 201
            
        except Exception as e:
            logger.error(f"Error al crear tarea: {str(e)}")
            return {
                'success': False,
                'error': 'Error interno del servidor',
                'message': str(e)
            }, 500
    
    def update_task(self, task_id: int) -> Tuple[Dict[str, Any], int]:
        """Actualiza una tarea existente"""
        try:
            data = request.get_json()
            
            if not data:
                return {
                    'success': False,
                    'error': 'No se proporcionaron datos para actualizar'
                }, 400
            
            # Validar prioridad si está presente
            if 'priority' in data and data['priority'] not in Task.VALID_PRIORITIES:
                return {
                    'success': False,
                    'error': f'Prioridad inválida. Valores permitidos: {", ".join(Task.VALID_PRIORITIES)}'
                }, 400
            
            # Validar estado si está presente
            if 'status' in data and data['status'] not in Task.VALID_STATUSES:
                return {
                    'success': False,
                    'error': f'Estado inválido. Valores permitidos: {", ".join(Task.VALID_STATUSES)}'
                }, 400
            
            updated_task = self.task_manager.update_task(task_id, data)
            
            if not updated_task:
                return {
                    'success': False,
                    'error': 'Tarea no encontrada'
                }, 404
            
            task_dict = updated_task.to_dict()
            # Convertir categoría a nombre de visualización
            category_display_names = TaskCategory.get_display_names()
            task_dict['category'] = category_display_names.get(task_dict['category'], 'Otro')
            
            return {
                'success': True,
                'data': task_dict,
                'message': 'Tarea actualizada exitosamente'
            }, 200
        
        except Exception as e:
            return {
                'success': False,
                'error': 'Error interno del servidor',
                'message': str(e)
            }, 500
    
    def delete_task(self, task_id: int) -> Tuple[Dict[str, Any], int]:
        """Elimina una tarea"""
        try:
            # Verificar que la tarea existe
            task = self.task_manager.get_task(task_id)
            if not task:
                return {
                    'success': False,
                    'error': 'Tarea no encontrada'
                }, 404
            
            success = self.task_manager.delete_task(task_id)
            
            if not success:
                return {
                    'success': False,
                    'error': 'Error al eliminar la tarea'
                }, 500
            
            return {
                'success': True,
                'message': 'Tarea eliminada exitosamente'
            }, 200
        
        except Exception as e:
            return {
                'success': False,
                'error': 'Error interno del servidor',
                'message': str(e)
            }, 500
    
    def get_stats(self) -> Tuple[Dict[str, Any], int]:
        """
        Obtiene estadísticas generales de las tareas.
        
        Returns:
            Tuple[Dict[str, Any], int]: Estadísticas y código de estado
        """
        logger.debug("Entrando a get_stats")
        try:
            tasks = self.task_manager.get_all_tasks()
            logger.debug(f"Tareas cargadas: {len(tasks)}")
            logger.debug(f"Tipo de tasks: {type(tasks)}")
            
            if not tasks:
                logger.warning("No se encontraron tareas")
                return {
                    'success': True,
                    'data': {
                        'total_tasks': 0,
                        'total_effort': 0,
                        'total_hours_incomplete': 0,
                        'status_counts': {},
                        'priority_counts': {},
                        'assigned_hours': {},
                        'tokens_por_tarea': [],
                        'costos_por_tarea': [],
                        'titulos_tareas': []
                    }
                }, 200
            
            # Imprimir detalles de cada tarea
            for task in tasks:
                logger.debug(f"Tarea ID {task['id']}: assigned_to='{task['assigned_to']}', effort={task['effort']}")
            
            # Estadísticas básicas
            total_tasks = len(tasks)
            total_hours = sum(task['effort'] for task in tasks)

            # Calcular horas solo para tareas no completadas
            total_hours_incomplete = sum(task['effort'] for task in tasks if task['status'] != 'completada')
            
            # Conteo por estado
            status_counts = {}
            for task in tasks:
                status_counts[task['status']] = status_counts.get(task['status'], 0) + 1
            
            # Conteo por prioridad
            priority_counts = {}
            for task in tasks:
                priority_counts[task['priority']] = priority_counts.get(task['priority'], 0) + 1
            
            # Horas por persona asignada
            assigned_hours = {}
            logger.debug("Iniciando bucle de assigned_hours")
            for task in tasks:
                person = task['assigned_to'] or 'Sin asignar'
                logger.debug(f"Procesando tarea {task['id']}, assigned_to='{person}', effort={task['effort']}")
                assigned_hours[person] = assigned_hours.get(person, 0) + task['effort']
            
            logger.debug(f"assigned_hours final: {assigned_hours}")

            # Tokens, costos y títulos de tareas
            tokens_por_tarea = [task.get('tokens_gastados', 0) or 0 for task in tasks]
            costos_por_tarea = [float(task.get('costos', 0.0) or 0.0) for task in tasks]
            titulos_tareas = [task['title'] for task in tasks]

            data_to_return = {
                'total_tasks': total_tasks,
                'total_effort': total_hours,
                'total_hours_incomplete': total_hours_incomplete,
                'status_counts': status_counts,
                'priority_counts': priority_counts,
                'assigned_hours': assigned_hours,
                'tokens_por_tarea': tokens_por_tarea,
                'costos_por_tarea': costos_por_tarea,
                'titulos_tareas': titulos_tareas
            }

            logger.debug(f"Datos a retornar: {data_to_return}")

            return {
                'success': True,
                'data': data_to_return
            }, 200
            
        except Exception as e:
            logger.error(f"Error al obtener estadísticas: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': 'Error al obtener estadísticas'
            }, 500

    def generate_description(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """Genera una descripción para la tarea usando el servicio de IA"""
        try:
            if not data or 'title' not in data:
                return {
                    'success': False,
                    'error': 'Se requiere el título de la tarea'
                }, 400
            
            ai_service = AIService()
            result = ai_service.generate_description(data['title'])
            
            if result['success']:
                return {
                    'success': True,
                    'description': result['description']
                }, 200
            else:
                return {
                    'success': False,
                    'error': result['error']
                }, 500
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }, 500

    def estimate_effort(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """Estima el esfuerzo necesario para la tarea usando el servicio de IA"""
        try:
            if not data or 'title' not in data:
                return {
                    'success': False,
                    'error': 'Se requiere el título de la tarea'
                }, 400
            
            ai_service = AIService()
            result = ai_service.estimate_effort(
                data['title'],
                data.get('description', ''),
                data.get('category', '')
            )
            
            if result['success']:
                return {
                    'success': True,
                    'effort': result['effort']
                }, 200
            else:
                return {
                    'success': False,
                    'error': result['error']
                }, 500
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }, 500

    def analyze_risks(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """Analiza los riesgos de la tarea usando el servicio de IA"""
        try:
            if not data or 'title' not in data:
                return {
                    'success': False,
                    'error': 'Se requiere el título de la tarea'
                }, 400
            
            ai_service = AIService()
            result = ai_service.analyze_risks(
                data['title'],
                data.get('description', ''),
                data.get('category', '')
            )
            
            if result['success']:
                return {
                    'success': True,
                    'risk_analysis': result['risk_analysis']
                }, 200
            else:
                return {
                    'success': False,
                    'error': result['error']
                }, 500
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }, 500

    def generate_mitigation(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """Genera un plan de mitigación usando el servicio de IA"""
        try:
            if not data or 'risk_analysis' not in data:
                return {
                    'success': False,
                    'error': 'Se requiere el análisis de riesgos'
                }, 400
            
            ai_service = AIService()
            result = ai_service.generate_mitigation(
                data.get('title', ''),
                data.get('description', ''),
                data.get('category', ''),
                data['risk_analysis']
            )
            
            if result['success']:
                return {
                    'success': True,
                    'mitigation_plan': result['mitigation_plan']
                }, 200
            else:
                return {
                    'success': False,
                    'error': result['error']
                }, 500
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }, 500

    def categorize_task(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """Clasifica una tarea basándose en su título y descripción"""
        try:
            if not data or 'title' not in data:
                return {
                    'success': False,
                    'error': 'Se requiere el título de la tarea'
                }, 400
            
            ai_service = AIService()
            result = ai_service.categorize_task(
                data['title'],
                data.get('description', '')
            )
            
            if result['success']:
                return {
                    'success': True,
                    'category': result['category']
                }, 200
            else:
                return {
                    'success': False,
                    'error': result['error']
                }, 500
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }, 500

    def enrich_task(self, task_id):
        db = get_db_session()
        task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
        if not task:
            return "Tarea no encontrada", 404
        ai_service = AIService()
        # Llamar a IA para enriquecer la tarea
        enriched = ai_service.process_task({
            'title': task.title
        })
        task.description = enriched.get('description', task.description)
        task.category = enriched.get('category', task.category)
        task.effort = enriched.get('effort', task.effort)
        task.risk_analysis = enriched.get('risk_analysis', task.risk_analysis)
        task.mitigation_plan = enriched.get('risk_mitigation', task.mitigation_plan)
        task.tokens_gastados = enriched.get('tokens_gastados', task.tokens_gastados)
        task.costos = enriched.get('costos', task.costos)
        db.commit()
        return redirect(url_for('user_story_routes.tasks_for_user_story', user_story_id=task.user_story_id))