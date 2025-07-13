from app.models.user_story_db import UserStory
from app.models.task_db import TaskDB
from app.models.task_db import StatusEnum, PriorityEnum
from app.models.enums import TaskCategory
from app.schemas.user_story_schema import UserStorySchema
from app.database.azure_connection import get_db_session
from sqlalchemy.orm import Session
from typing import List, Optional

class UserStoryService:
    def __init__(self, db: Optional[Session] = None):
        self.db = db or get_db_session()
        
        # Inicializar el servicio de IA de forma segura
        try:
            from app.services.ai_service import AIService
            self.ai_service = AIService()
            print("✅ Servicio de IA inicializado en UserStoryService")
        except Exception as e:
            print(f"⚠️ Error al inicializar el servicio de IA en UserStoryService: {str(e)}")
            print("⚠️ Las funcionalidades de IA estarán deshabilitadas")
            self.ai_service = None

    def get_all_user_stories(self) -> List[UserStory]:
        return self.db.query(UserStory).order_by(UserStory.created_at.desc()).all()

    def create_user_story(self, user_story_data: dict) -> UserStory:
        user_story = UserStory(**user_story_data)
        self.db.add(user_story)
        self.db.commit()
        self.db.refresh(user_story)
        return user_story

    def get_user_story(self, user_story_id: int) -> Optional[UserStory]:
        return self.db.query(UserStory).filter(UserStory.id == user_story_id).first()

    def generate_user_story_from_prompt(self, prompt: str) -> UserStory:
        if not self.ai_service:
            raise Exception("Servicio de IA no disponible")
            
        # Prompt en español para Azure OpenAI
        prompt_ia = f"Genera una historia de usuario en formato JSON con los campos: project, role, goal, reason, description, priority (baja, media, alta, bloqueante), story_points (1-8), effort_hours (decimal). Prompt: {prompt}"
        result = self.ai_service.generate_user_story(prompt_ia)
        user_story_data = result  # Se espera que sea un dict válido
        return self.create_user_story(user_story_data)

    def generate_tasks_for_user_story(self, user_story_id: int) -> list:
        try:
            if not self.ai_service:
                print("⚠️ Servicio de IA no disponible para generar tareas")
                return []
                
            user_story = self.get_user_story(user_story_id)
            if not user_story:
                print(f"User story {user_story_id} no encontrada")
                return []
            
            prompt_ia = (
                f"Genera una lista de tareas en formato JSON para la siguiente historia de usuario: "
                f"Proyecto: {user_story.project}, Rol: {user_story.role}, Objetivo: {user_story.goal}, Razón: {user_story.reason}, Descripción: {user_story.description}. "
            )
            
            print(f"Generando tareas para user story {user_story_id}")
            print(f"Prompt: {prompt_ia}")
            
            tasks_data = self.ai_service.generate_tasks(prompt_ia)
            print(f"Tareas generadas por IA: {tasks_data}")
            
            tasks = []
            for i, task_data in enumerate(tasks_data):
                # Si el modelo devuelve solo strings, conviértelo a dict
                if isinstance(task_data, str):
                    task_data = {"title": task_data, "description": ""}
                
                # Asegurar que tenemos al menos un título
                title = task_data.get("title", f"Tarea {i+1}")
                description = task_data.get("description", "")
                
                print(f"Creando tarea {i+1}: {title}")
                
                # Generar categoría usando IA
                try:
                    if self.ai_service:
                        category_result = self.ai_service.categorize_task(title, description)
                        if category_result.get('success'):
                            category_value = category_result['category']
                        else:
                            category_value = 'otro'
                    else:
                        category_value = 'otro'
                except:
                    category_value = 'otro'
                
                # Convertir string a enum TaskCategory
                try:
                    category_enum = TaskCategory(category_value)
                except ValueError:
                    category_enum = TaskCategory.OTRO
                
                task = TaskDB(
                    title=title,
                    description=description,
                    user_story_id=user_story_id,
                    status=StatusEnum.PENDIENTE,
                    priority=PriorityEnum.MEDIA,
                    category=category_enum
                )
                self.db.add(task)
                tasks.append(task)
            
            self.db.commit()
            print(f"Se guardaron {len(tasks)} tareas en la base de datos")
            return tasks
            
        except Exception as e:
            print(f"Error generando tareas: {str(e)}")
            self.db.rollback()
            return []

    def get_tasks_for_user_story(self, user_story_id: int) -> List[TaskDB]:
        return self.db.query(TaskDB).filter(TaskDB.user_story_id == user_story_id).all()

    def generate_user_story_with_fields(self, data: dict) -> dict:
        if not self.ai_service:
            return None
            
        # Construir el prompt para la IA usando los campos individuales
        prompt_ia = (
            f"Genera una historia de usuario en formato JSON con los campos: "
            f"project, role, goal, reason, description, priority (baja, media, alta, bloqueante), "
            f"story_points (1-8), effort_hours (decimal). "
            f"\nProyecto: {data.get('project')}\nRol: {data.get('role')}\nObjetivo: {data.get('goal')}\nRazón: {data.get('reason')}\n" 
            f"Prompt adicional: {data.get('prompt')}"
        )
        result = self.ai_service.generate_user_story(prompt_ia)
        # Se espera que result sea un dict con los campos requeridos
        if not result or not isinstance(result, dict):
            return None
        # Validar que los campos requeridos estén presentes
        required = ['description', 'priority', 'story_points', 'effort_hours']
        if not all(field in result for field in required):
            return None
        # Devolver todos los datos para el frontend
        return {
            "project": data.get('project'),
            "role": data.get('role'),
            "goal": data.get('goal'),
            "reason": data.get('reason'),
            "description": result.get('description'),
            "priority": result.get('priority'),
            "story_points": result.get('story_points'),
            "effort_hours": result.get('effort_hours')
        } 