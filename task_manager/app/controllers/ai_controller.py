from flask import Blueprint, request, jsonify, session
from app.services.ai_service import AIService
from app.models.task import Task
from app.models.enums import TaskCategory
import uuid
import json
from flask import current_app

ai_bp = Blueprint('ai', __name__)
ai_service = AIService()

# Utilidad para cargar y guardar tareas en el JSON
TASKS_JSON_PATH = 'data/tasks.json'
def load_tasks():
    with open(TASKS_JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)
def save_tasks(tasks):
    with open(TASKS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# Diccionario en memoria para tokens/costos por formulario
formulario_stats = {}

def reset_token_cost_totals():
    session['total_tokens'] = 0
    session['total_cost'] = 0.0

def update_token_cost_totals(tokens, cost):
    session['total_tokens'] = session.get('total_tokens', 0) + tokens
    session['total_cost'] = session.get('total_cost', 0.0) + cost

@ai_bp.route('/reset-totals', methods=['POST'])
def reset_totals():
    reset_token_cost_totals()
    return jsonify({'success': True})

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
    """Genera una descripción detallada para una tarea"""
    try:
        data = request.get_json()
        form_id = data.get('form_id')
        result = ai_service.generate_description(data.get('title', ''))
        
        # Agregar logs para depuración
        print("\n=== Datos recibidos del servicio AI ===")
        print(f"Result completo: {result}")
        print("=====================================\n")
        
        if result['success'] and form_id in formulario_stats:
            formulario_stats[form_id]['tokens'][0] = result['total_tokens']
            formulario_stats[form_id]['costs'][0] = result['cost']
            total_tokens = sum(formulario_stats[form_id]['tokens'])
            total_cost = sum(formulario_stats[form_id]['costs'])
            response_data = {
                'success': True,
                'description': result['description'],
                'total_tokens': total_tokens,
                'cost': total_cost,
                'form_id': form_id
            }
            
            # Agregar logs para depuración
            print("\n=== Datos enviados al frontend ===")
            print(f"Response data: {response_data}")
            print("================================\n")
            
            return jsonify(response_data)
        else:
            return jsonify({'success': False, 'error': result.get('error', 'Error de formulario')}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ai_bp.route('/categorize', methods=['POST'])
def categorize():
    try:
        data = request.get_json()
        form_id = data.get('form_id')
        result = ai_service.categorize_task(
            data.get('title', ''),
            data.get('description', '')
        )
        if result['success'] and form_id in formulario_stats:
            formulario_stats[form_id]['tokens'][1] = result['total_tokens']
            formulario_stats[form_id]['costs'][1] = result['cost']
            total_tokens = sum(formulario_stats[form_id]['tokens'])
            total_cost = sum(formulario_stats[form_id]['costs'])
            return jsonify({
                'success': True,
                'category': result['category'],
                'total_tokens': total_tokens,
                'cost': total_cost,
                'form_id': form_id
            })
        else:
            return jsonify({'success': False, 'error': result.get('error', 'Error de formulario')}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ai_bp.route('/estimate-effort', methods=['POST'])
def estimate_effort():
    try:
        data = request.get_json()
        form_id = data.get('form_id')
        result = ai_service.estimate_effort(
            data.get('title', ''),
            data.get('description', ''),
            data.get('category', '')
        )
        if result['success'] and form_id in formulario_stats:
            formulario_stats[form_id]['tokens'][2] = result['total_tokens']
            formulario_stats[form_id]['costs'][2] = result['cost']
            total_tokens = sum(formulario_stats[form_id]['tokens'])
            total_cost = sum(formulario_stats[form_id]['costs'])
            return jsonify({
                'success': True,
                'effort': result['effort'],
                'total_tokens': total_tokens,
                'cost': total_cost,
                'form_id': form_id
            })
        else:
            return jsonify({'success': False, 'error': result.get('error', 'Error de formulario')}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ai_bp.route('/analyze-risks', methods=['POST'])
def analyze_risks():
    try:
        data = request.get_json()
        form_id = data.get('form_id')
        result = ai_service.analyze_risks(
            data.get('title', ''),
            data.get('description', ''),
            data.get('category', '')
        )
        if result['success'] and form_id in formulario_stats:
            formulario_stats[form_id]['tokens'][3] = result['total_tokens']
            formulario_stats[form_id]['costs'][3] = result['cost']
            total_tokens = sum(formulario_stats[form_id]['tokens'])
            total_cost = sum(formulario_stats[form_id]['costs'])
            return jsonify({
                'success': True,
                'risk_analysis': result['risk_analysis'],
                'total_tokens': total_tokens,
                'cost': total_cost,
                'form_id': form_id
            })
        else:
            return jsonify({'success': False, 'error': result.get('error', 'Error de formulario')}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ai_bp.route('/generate-mitigation', methods=['POST'])
def generate_mitigation():
    try:
        data = request.get_json()
        form_id = data.get('form_id')
        
        print(f"\n=== GENERATE MITIGATION DEBUG ===")
        print(f"Datos recibidos: {data}")
        print(f"Form ID: {form_id}")
        
        result = ai_service.generate_mitigation(
            data.get('title', ''),
            data.get('description', ''),
            data.get('category', ''),
            data.get('risk_analysis', '')
        )
        
        print(f"Resultado del servicio AI: {result}")
        
        if result['success'] and form_id in formulario_stats:
            print(f"Procesando respuesta exitosa...")
            formulario_stats[form_id]['tokens'][4] = result['total_tokens']
            formulario_stats[form_id]['costs'][4] = result['cost']
            total_tokens = sum(formulario_stats[form_id]['tokens'])
            total_cost = sum(formulario_stats[form_id]['costs'])
            
            print(f"Tokens totales: {total_tokens}, Costo total: {total_cost}")
            
            # Guardar en el JSON
            tasks = load_tasks()
            # Buscar la tarea por form_id y actualizar tokens/costos
            for task in tasks:
                if task.get('form_id') == form_id:
                    task['tokens_por_llamada'] = formulario_stats[form_id]['tokens']
                    task['costos_por_llamada'] = formulario_stats[form_id]['costs']
                    task['total_tokens'] = total_tokens
                    task['total_cost'] = total_cost
                    break
            else:
                # Si no existe, crear nueva entrada
                tasks.append({
                    'form_id': form_id,
                    'tokens_por_llamada': formulario_stats[form_id]['tokens'],
                    'costos_por_llamada': formulario_stats[form_id]['costs'],
                    'total_tokens': total_tokens,
                    'total_cost': total_cost
                })
            save_tasks(tasks)
            
            response_data = {
                'success': True,
                'mitigation_plan': result['mitigation_plan'],
                'total_tokens': total_tokens,
                'cost': total_cost,
                'form_id': form_id
            }
            
            print(f"Respuesta a enviar: {response_data}")
            print("=====================================\n")
            
            return jsonify(response_data)
        else:
            print(f"Error en el resultado: {result}")
            error_msg = result.get('error', 'Error desconocido')
            # Proporcionar mensajes más específicos para errores comunes
            if '429' in error_msg or 'Too Many Requests' in error_msg:
                error_msg = "Se ha excedido el límite de solicitudes a Azure OpenAI. Por favor, espera un momento antes de intentar nuevamente."
            elif 'timeout' in error_msg.lower():
                error_msg = "La solicitud ha excedido el tiempo de espera. Intenta nuevamente."
            elif 'quota' in error_msg.lower():
                error_msg = "Se ha excedido la cuota de Azure OpenAI. Verifica tu plan de suscripción."
            
            print(f"Mensaje de error final: {error_msg}")
            print("=====================================\n")
            
            return jsonify({'success': False, 'error': error_msg}), 500
    except Exception as e:
        print(f"Excepción capturada: {str(e)}")
        error_msg = str(e)
        # Proporcionar mensajes más específicos para errores comunes
        if '429' in error_msg or 'Too Many Requests' in error_msg:
            error_msg = "Se ha excedido el límite de solicitudes a Azure OpenAI. Por favor, espera un momento antes de intentar nuevamente."
        elif 'timeout' in error_msg.lower():
            error_msg = "La solicitud ha excedido el tiempo de espera. Intenta nuevamente."
        elif 'quota' in error_msg.lower():
            error_msg = "Se ha excedido la cuota de Azure OpenAI. Verifica tu plan de suscripción."
        
        print(f"Mensaje de error final: {error_msg}")
        print("=====================================\n")
        
        return jsonify({'success': False, 'error': error_msg}), 500 