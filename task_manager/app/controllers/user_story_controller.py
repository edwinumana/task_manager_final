from flask import request, render_template, redirect, url_for, jsonify
from app.services.user_story_service import UserStoryService
from app.models.enums import TaskCategory

class UserStoryController:
    def __init__(self):
        self.service = UserStoryService()

    def list_user_stories(self):
        user_stories = self.service.get_all_user_stories()
        for story in user_stories:
            story.tasks = self.service.get_tasks_for_user_story(story.id)
        return render_template('user-stories.html', user_stories=user_stories)

    def create_user_story(self):
        prompt = request.form.get('prompt')
        if prompt:
            self.service.generate_user_story_from_prompt(prompt)
        return redirect(url_for('user_story_routes.list_user_stories'))

    def generate_tasks(self, user_story_id):
        self.service.generate_tasks_for_user_story(user_story_id)
        return redirect(url_for('user_story_routes.tasks_for_user_story', user_story_id=user_story_id))

    def tasks_for_user_story(self, user_story_id):
        # Obtener la User Story
        user_story = self.service.get_user_story(user_story_id)
        if not user_story:
            return redirect(url_for('user_story_routes.list_user_stories'))
        
        # Obtener las tareas asociadas a esta User Story
        tasks = self.service.get_tasks_for_user_story(user_story_id)
        
        # Convertir las tareas a diccionarios con información de la User Story
        tasks_with_us_data = []
        category_display_names = TaskCategory.get_display_names()
        
        for task in tasks:
            task_dict = task.to_dict()
            # Añadir información de la User Story
            task_dict['user_story_project'] = user_story.project
            task_dict['user_story_role'] = user_story.role
            task_dict['user_story_goal'] = user_story.goal
            task_dict['user_story_reason'] = user_story.reason
            task_dict['user_story_priority'] = user_story.priority.value if user_story.priority else ''
            task_dict['user_story_description'] = user_story.description
            # Convertir categoría a nombre de visualización
            # task_dict['category'] ya contiene el valor interno del enum (ej: 'testing')
            # Necesitamos convertirlo al nombre de visualización
            original_category = task_dict['category']
            
            # Mapeo robusto que maneja cualquier valor de categoría
            category_mapping = {
                # Valores internos del enum
                'testing': 'Testing y Control de Calidad',
                'frontend': 'Desarrollo Frontend',
                'backend': 'Desarrollo Backend',
                'desarrollo': 'Desarrollo General',
                'diseño': 'Diseño de Sistemas',
                'documentacion': 'Documentación',
                'base_de_datos': 'Base de Datos',
                'seguridad': 'Seguridad',
                'infraestructura': 'Infraestructura',
                'mantenimiento': 'Mantenimiento',
                'investigacion': 'Investigación',
                'supervision': 'Supervisión',
                'riesgos_laborales': 'Riesgos Laborales',
                'limpieza': 'Limpieza',
                'otro': 'Otro',
                # Valores antiguos que podrían estar en la base de datos
                'TESTING': 'Testing y Control de Calidad',
                'DESARROLLO': 'Desarrollo General',
                'DOCUMENTACION': 'Documentación',
                'REUNION': 'Reunión',
                'OTRO': 'Otro'
            }
            
            task_dict['category'] = category_mapping.get(original_category, 'Otro')
            # Formatear fecha de creación
            if task.created_at:
                task_dict['created_at'] = task.created_at.strftime('%d/%m/%Y %H:%M')
            else:
                task_dict['created_at'] = ''
            tasks_with_us_data.append(task_dict)
        
        return render_template('tasks/list.html', 
                             tasks=tasks_with_us_data, 
                             user_story_id=user_story_id,
                             user_story=user_story)

    def generate_user_story_ia(self):
        try:
            data = request.get_json()
            required_fields = ['project', 'role', 'goal', 'reason', 'prompt']
            if not all(field in data for field in required_fields):
                return jsonify({"success": False, "error": "Faltan campos requeridos."}), 400
            result = self.service.generate_user_story_with_fields(data)
            if not result:
                return jsonify({"success": False, "error": "No se pudo generar la historia de usuario con IA."}), 500
            return jsonify({"success": True, "data": result}), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    def create_user_story_json(self):
        try:
            data = request.get_json()
            required_fields = ['project', 'role', 'goal', 'reason', 'description', 'priority', 'story_points', 'effort_hours']
            if not all(field in data for field in required_fields):
                return jsonify({"success": False, "error": "Faltan campos requeridos para guardar la historia de usuario."}), 400
            user_story = self.service.create_user_story(data)
            return jsonify({"success": True, "data": {"id": user_story.id, "message": "Historia de usuario guardada correctamente"}}), 201
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500 