from flask import Blueprint, request, jsonify
from app.models.task import Task
from app.utils.task_manager import TaskManager
import uuid
import json

# Crear el Blueprint
ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

# Inicializar el servicio de IA de forma segura
try:
    from app.services.ai_service import AIService
    ai_service = AIService()
    print("✅ Servicio de IA inicializado correctamente")
except Exception as e:
    print(f"⚠️ Error al inicializar el servicio de IA: {str(e)}")
    print("⚠️ La aplicación continuará sin funcionalidades de IA")
    ai_service = None

# Diccionario en memoria para tokens/costos por formulario
formulario_stats = {}
TASKS_JSON_PATH = 'data/tasks.json'
def load_tasks():
    with open(TASKS_JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)
def save_tasks(tasks):
    with open(TASKS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def handle_ai_error(error_msg):
    """Función utilitaria para manejar errores de IA con mensajes específicos"""
    if '429' in error_msg or 'Too Many Requests' in error_msg:
        return "Se ha excedido el límite de solicitudes a Azure OpenAI. Por favor, espera un momento antes de intentar nuevamente."
    elif 'timeout' in error_msg.lower():
        return "La solicitud ha excedido el tiempo de espera. Intenta nuevamente."
    elif 'quota' in error_msg.lower():
        return "Se ha excedido la cuota de Azure OpenAI. Verifica tu plan de suscripción."
    return error_msg

def process_ai_response(result, form_id, token_index):
    """Función utilitaria para procesar respuestas de IA"""
    if not result['success']:
        error_msg = handle_ai_error(result.get('error', 'Error desconocido'))
        return jsonify({'success': False, 'error': error_msg}), 500
    
    if form_id not in formulario_stats:
        return jsonify({'success': False, 'error': 'Error de formulario: form_id no encontrado'}), 500
    
    formulario_stats[form_id]['tokens'][token_index] = result['total_tokens']
    formulario_stats[form_id]['costs'][token_index] = result['cost']
    total_tokens = sum(formulario_stats[form_id]['tokens'])
    total_cost = sum(formulario_stats[form_id]['costs'])
    
    return total_tokens, total_cost

@ai_bp.route('/create-form', methods=['POST'])
def create_form():
    form_id = str(uuid.uuid4())
    formulario_stats[form_id] = {
        'tokens': [0, 0, 0, 0, 0],
        'costs': [0.0, 0.0, 0.0, 0.0, 0.0]
    }
    return jsonify({'success': True, 'form_id': form_id})

@ai_bp.route('/generate-description', methods=['POST'])
def generate_description():
    """Endpoint para generar una descripción con IA"""
    try:
        if ai_service is None:
            return jsonify({'success': False, 'error': 'Servicio de IA no disponible'}), 503
            
        data = request.get_json()
        form_id = data.get('form_id')
        
        if not data or 'title' not in data or not form_id:
            return jsonify({'error': 'Se requiere el título de la tarea y form_id'}), 400
        
        result = ai_service.generate_description(data['title'])
        response = process_ai_response(result, form_id, 0)
        
        if isinstance(response, tuple) and len(response) == 2 and isinstance(response[0], int):
            total_tokens, total_cost = response
            return jsonify({
                'success': True,
                'description': result['description'],
                'total_tokens': total_tokens,
                'cost': total_cost,
                'form_id': form_id
            })
        else:
            return response
            
    except Exception as e:
        error_msg = handle_ai_error(str(e))
        return jsonify({'success': False, 'error': error_msg}), 500

@ai_bp.route('/categorize', methods=['POST'])
def categorize():
    """Endpoint para categorizar una tarea con IA"""
    try:
        if ai_service is None:
            return jsonify({'success': False, 'error': 'Servicio de IA no disponible'}), 503
            
        data = request.get_json()
        form_id = data.get('form_id')
        
        if not data or 'title' not in data or not form_id:
            return jsonify({'error': 'Se requiere el título de la tarea y form_id'}), 400
        
        result = ai_service.categorize_task(data['title'])
        response = process_ai_response(result, form_id, 1)
        
        if isinstance(response, tuple) and len(response) == 2 and isinstance(response[0], int):
            total_tokens, total_cost = response
            return jsonify({
                'success': True,
                'category': result['category'],
                'total_tokens': total_tokens,
                'cost': total_cost,
                'form_id': form_id
            })
        else:
            return response
            
    except Exception as e:
        error_msg = handle_ai_error(str(e))
        return jsonify({'success': False, 'error': error_msg}), 500

@ai_bp.route('/estimate-effort', methods=['POST'])
def estimate_effort():
    """Endpoint para estimar el esfuerzo con IA"""
    try:
        if ai_service is None:
            return jsonify({'success': False, 'error': 'Servicio de IA no disponible'}), 503
            
        data = request.get_json()
        form_id = data.get('form_id')
        
        if not data or 'title' not in data or not form_id:
            return jsonify({'error': 'Se requiere el título de la tarea y form_id'}), 400
        
        result = ai_service.estimate_effort(data['title'], data.get('description', ''))
        response = process_ai_response(result, form_id, 2)
        
        if isinstance(response, tuple) and len(response) == 2 and isinstance(response[0], int):
            total_tokens, total_cost = response
            return jsonify({
                'success': True,
                'effort': result['effort'],
                'total_tokens': total_tokens,
                'cost': total_cost,
                'form_id': form_id
            })
        else:
            return response
            
    except Exception as e:
        error_msg = handle_ai_error(str(e))
        return jsonify({'success': False, 'error': error_msg}), 500

@ai_bp.route('/analyze-risks', methods=['POST'])
def analyze_risks():
    """Endpoint para analizar riesgos con IA"""
    try:
        if ai_service is None:
            return jsonify({'success': False, 'error': 'Servicio de IA no disponible'}), 503
            
        data = request.get_json()
        form_id = data.get('form_id')
        
        if not data or 'title' not in data or not form_id:
            return jsonify({'error': 'Se requiere el título de la tarea y form_id'}), 400
        
        result = ai_service.analyze_risks(
            data['title'],
            data.get('description', ''),
            data.get('category', '')
        )
        response = process_ai_response(result, form_id, 3)
        
        if isinstance(response, tuple) and len(response) == 2 and isinstance(response[0], int):
            total_tokens, total_cost = response
            return jsonify({
                'success': True,
                'risk_analysis': result['risk_analysis'],
                'total_tokens': total_tokens,
                'cost': total_cost,
                'form_id': form_id
            })
        else:
            return response
            
    except Exception as e:
        error_msg = handle_ai_error(str(e))
        return jsonify({'success': False, 'error': error_msg}), 500

@ai_bp.route('/generate-mitigation', methods=['POST'])
def generate_mitigation():
    """Endpoint para generar un plan de mitigación con IA"""
    try:
        if ai_service is None:
            return jsonify({'success': False, 'error': 'Servicio de IA no disponible'}), 503
            
        data = request.get_json()
        form_id = data.get('form_id')
        
        if not data or 'title' not in data or not form_id:
            return jsonify({'error': 'Se requiere el título de la tarea y form_id'}), 400
        
        result = ai_service.generate_mitigation(
            data['title'],
            data.get('description', ''),
            data.get('category', ''),
            data.get('risk_analysis', '')
        )
        response = process_ai_response(result, form_id, 4)
        
        if isinstance(response, tuple) and len(response) == 2 and isinstance(response[0], int):
            total_tokens, total_cost = response
            return jsonify({
                'success': True,
                'mitigation_plan': result['mitigation_plan'],
                'total_tokens': total_tokens,
                'cost': total_cost,
                'form_id': form_id
            })
        else:
            return response
            
    except Exception as e:
        error_msg = handle_ai_error(str(e))
        return jsonify({'success': False, 'error': error_msg}), 500

@ai_bp.route('/process-task', methods=['POST'])
def process_task():
    """Endpoint para procesar una tarea completa con IA"""
    try:
        if ai_service is None:
            return jsonify({'success': False, 'error': 'Servicio de IA no disponible'}), 503
            
        data = request.get_json()
        form_id = data.get('form_id')
        
        if not data:
            return jsonify({'error': 'Se requieren datos de la tarea'}), 400
        
        # Usar TaskManager para crear la tarea
        task_manager = TaskManager()
        
        # Crear tarea con los datos procesados por IA
        task_data = {
            'title': data.get('title', ''),
            'description': data.get('description', ''),
            'category': data.get('category', 'OTRO'),
            'priority': data.get('priority', 'media'),
            'status': data.get('status', 'pendiente'),
            'effort': data.get('effort', 0),
            'assigned_to': data.get('assigned_to', 'No asignado'),
            'risk_analysis': data.get('risk_analysis', ''),
            'mitigation_plan': data.get('mitigation_plan', ''),
            'tokens_gastados': data.get('total_tokens', 0),
            'costos': data.get('total_cost', 0.0),
            'user_story_id': data.get('user_story_id')
        }
        
        new_task = task_manager.create_task(task_data)
        
        if new_task:
            return jsonify({
                'success': True,
                'message': 'Tarea creada exitosamente',
                'task_id': new_task.id,
                'redirect_url': f'/tasks/{new_task.id}'
            })
        else:
            return jsonify({'success': False, 'error': 'Error al crear la tarea'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500 