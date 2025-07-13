from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app.controllers.task_controller import TaskController

# Crear el blueprint para las rutas de tareas
task_bp = Blueprint('tasks', __name__)

# Crear una instancia del controlador
task_controller = TaskController()

@task_bp.route('/')
def index():
    """Renderiza la página principal de tareas."""
    return render_template('tasks/index.html')

@task_bp.route('/list')
def list_tasks():
    """Renderiza la lista de tareas."""
    response, _ = task_controller.get_all_tasks()
    if response['success']:
        tasks = response['tasks']
        total_tokens = sum(task.get('tokens_gastados', 0) or 0 for task in tasks)
        total_costos = sum(float(task.get('costos', 0.0) or 0.0) for task in tasks)
        return render_template('tasks/list.html', tasks=tasks, total_tokens=total_tokens, total_costos=total_costos)
    flash('Error al cargar las tareas', 'error')
    return render_template('tasks/list.html', tasks=[], total_tokens=0, total_costos=0.0)

@task_bp.route('/<int:task_id>')
def view_task(task_id):
    """Renderiza la vista detallada de una tarea."""
    response, _ = task_controller.get_task_with_user_story(task_id)
    if response['success']:
        return render_template('tasks/view.html', task=response['data'])
    flash('Tarea no encontrada', 'error')
    return redirect(url_for('tasks.list_tasks'))

@task_bp.route('/stats')
def stats():
    """Renderiza la página de estadísticas."""
    return render_template('tasks/stats.html')



# Rutas de la API
@task_bp.route('/api/list')
def api_list_tasks():
    """Obtiene la lista de tareas en formato JSON."""
    response, status_code = task_controller.get_all_tasks()
    return jsonify(response), status_code

@task_bp.route('/api/<int:task_id>')
def api_get_task(task_id):
    """Obtiene una tarea específica en formato JSON."""
    response, status_code = task_controller.get_task_by_id(task_id)
    return jsonify(response), status_code

@task_bp.route('/api', methods=['POST'])
def api_create_task():
    """Crea una nueva tarea."""
    response, status_code = task_controller.create_task()
    return jsonify(response), status_code

@task_bp.route('/api/<int:task_id>', methods=['PUT'])
def api_update_task(task_id):
    """Actualiza una tarea existente."""
    response, status_code = task_controller.update_task(task_id)
    return jsonify(response), status_code

@task_bp.route('/api/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    """Elimina una tarea."""
    response, status_code = task_controller.delete_task(task_id)
    return jsonify(response), status_code

@task_bp.route('/api/stats')
def api_get_stats():
    """Obtiene estadísticas de las tareas."""
    response, status_code = task_controller.get_stats()
    return jsonify(response), status_code

# Rutas para las funciones del chatbot
@task_bp.route('/api/generate-description', methods=['POST'])
def api_generate_description():
    """Genera una descripción de la tarea."""
    data = request.get_json()
    response, status_code = task_controller.generate_description(data)
    return jsonify(response), status_code

@task_bp.route('/api/estimate-effort', methods=['POST'])
def api_estimate_effort():
    """Estima el esfuerzo necesario para completar la tarea."""
    data = request.get_json()
    response, status_code = task_controller.estimate_effort(data)
    return jsonify(response), status_code

@task_bp.route('/api/analyze-risks', methods=['POST'])
def api_analyze_risks():
    """Analiza los riesgos asociados a la tarea."""
    data = request.get_json()
    response, status_code = task_controller.analyze_risks(data)
    return jsonify(response), status_code

@task_bp.route('/api/generate-mitigation', methods=['POST'])
def api_generate_mitigation():
    """Genera un plan de mitigación para la tarea."""
    data = request.get_json()
    response, status_code = task_controller.generate_mitigation(data)
    return jsonify(response), status_code

@task_bp.route('/api/categorize', methods=['POST'])
def api_categorize_task():
    """Clasifica una tarea basándose en su título y descripción."""
    data = request.get_json()
    response, status_code = task_controller.categorize_task(data)
    return jsonify(response), status_code

@task_bp.route('/tasks/<int:task_id>/enrich', methods=['POST'])
def enrich_task(task_id):
    return task_controller.enrich_task(task_id)