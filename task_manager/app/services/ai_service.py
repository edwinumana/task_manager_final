import os
from typing import Dict, Any, Optional, Tuple
import openai
from dotenv import load_dotenv
from app.models.enums import TaskCategory
import tiktoken

# Cargar variables de entorno
load_dotenv()

class AIService:
    """Servicio para interactuar con Azure OpenAI"""
    
    def __init__(self):
        """Inicializa el cliente de Azure OpenAI"""
        try:
            # Verificar si estamos en modo testing
            is_testing = os.getenv("TESTING", "false").lower() == "true" or \
                        os.getenv("FLASK_ENV") == "testing"
            
            if is_testing:
                # En modo testing, usar valores por defecto
                print("🧪 Modo testing detectado - usando configuración mock para AIService")
                self._setup_testing_mode()
                return
            
            # Obtener las credenciales del archivo .env
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            api_version = os.getenv("AZURE_OPENAI_API_VERSION")
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            
            # Verificar que todas las credenciales estén presentes
            if not all([api_key, api_version, azure_endpoint]):
                raise ValueError("Faltan credenciales de Azure OpenAI en el archivo .env")
            
            # Configurar OpenAI para Azure (versión 0.28.1)
            openai.api_type = "azure"
            openai.api_key = api_key
            openai.api_base = azure_endpoint
            openai.api_version = api_version
            
            self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
            if not self.deployment_name:
                raise ValueError("Falta el nombre del deployment en el archivo .env")
            
            self.is_testing = False
            self._setup_production_mode()
            
        except Exception as e:
            print(f"Error al inicializar AIService: {e}")
            raise
    
    def _setup_testing_mode(self):
        """Configura el servicio para modo testing"""
        self.api_key = "test_key"
        self.api_version = "2023-12-01-preview"
        self.azure_endpoint = "https://test.openai.azure.com/"
        self.deployment_name = "test-deployment"
        self.is_testing = True
        
        # Atributos esperados por los tests
        self.client = None  # Mock client
        self.temperature = 0.7
        self.max_tokens = 1000
        
        # Configuración adicional del modelo (igual que en producción)
        self.top_p = float(os.getenv("TOP_P", "0.2"))
        self.frequency_penalty = float(os.getenv("FREQUENCY_PENALTY", "0.0"))
        self.presence_penalty = float(os.getenv("PRESENCE_PENALTY", "0.0"))
        
        # Configurar encoding para testing
        try:
            self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        except:
            self.encoding = None
    
    def _setup_production_mode(self):
        """Configura el servicio para modo producción"""
        self.is_testing = False
        
        # Atributos esperados por los tests
        self.client = openai  # Cliente real
        self.temperature = 0.7
        self.max_tokens = 1000
        
        # Configuración adicional del modelo
        self.top_p = float(os.getenv("TOP_P", "0.2"))
        self.frequency_penalty = float(os.getenv("FREQUENCY_PENALTY", "0.0"))
        self.presence_penalty = float(os.getenv("PRESENCE_PENALTY", "0.0"))
        
        # Configurar encoding
        try:
            self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        except:
            self.encoding = None

    def _mock_llm_response(self, system_prompt: str, user_prompt: str) -> Tuple[str, Dict[str, Any]]:
        """Respuesta mock para modo testing"""
        mock_response = f"Mock response for: {user_prompt[:50]}..."
        mock_usage = {
            'prompt_tokens': 50,
            'completion_tokens': 20,
            'total_tokens': 70
        }
        return mock_response, {'usage': mock_usage}

    def _call_llm(self, system_prompt: str, user_prompt: str) -> Tuple[str, Dict[str, Any]]:
        """Llama al LLM de Azure OpenAI"""
        
        # Si estamos en modo testing, usar respuesta mock
        if self.is_testing:
            return self._mock_llm_response(system_prompt, user_prompt)
        
        try:
            # Llamada real a OpenAI
            response = openai.ChatCompletion.create(
                engine=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
                stop=None
            )
            
            # Extraer la respuesta y estadísticas
            content = response.choices[0].message.content.strip()
            usage = response.usage
            
            # Calcular estadísticas
            stats = {
                'input_tokens': usage.prompt_tokens,
                'output_tokens': usage.completion_tokens,
                'total_tokens': usage.total_tokens,
                'cost': self.calculate_cost(usage.prompt_tokens, usage.completion_tokens)
            }
            
            return content, stats
            
        except Exception as e:
            # Manejar diferentes tipos de errores de OpenAI
            error_msg = str(e)
            if "rate limit" in error_msg.lower():
                print(f"Error de límite de velocidad: {e}")
                raise Exception("Límite de velocidad excedido. Intente nuevamente más tarde.")
            elif "authentication" in error_msg.lower() or "unauthorized" in error_msg.lower():
                print(f"Error de autenticación: {e}")
                raise Exception("Error de autenticación con Azure OpenAI.")
            elif "api" in error_msg.lower():
                print(f"Error de API: {e}")
                raise Exception("Error en la API de Azure OpenAI.")
            else:
                print(f"Error inesperado: {e}")
                raise Exception(f"Error inesperado al llamar a la API: {str(e)}")

    def count_tokens(self, text: str) -> int:
        """Cuenta los tokens en un texto"""
        if self.encoding is None:
            # Fallback: aproximación simple
            return int(len(text.split()) * 1.3)  # Aproximación
        try:
            return len(self.encoding.encode(text))
        except:
            return int(len(text.split()) * 1.3)  # Fallback

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calcula el costo aproximado de la llamada"""
        # Precios aproximados para GPT-3.5-turbo (pueden variar)
        input_cost_per_1k = 0.0015  # $0.0015 por 1K tokens de entrada
        output_cost_per_1k = 0.002  # $0.002 por 1K tokens de salida
        
        input_cost = (input_tokens / 1000) * input_cost_per_1k
        output_cost = (output_tokens / 1000) * output_cost_per_1k
        
        return input_cost + output_cost

    def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa una tarea completa con todas las funcionalidades de IA
        
        Args:
            task_data: Diccionario con los datos de la tarea
            
        Returns:
            Dict[str, Any]: Datos de la tarea procesados
        """
        try:
            # Generar descripción
            description, desc_info = self._call_llm(
                "Eres un experto en gestión de tareas. Genera una descripción profesional de máximo 300 palabras a partir de la tarea que te da el usuario.",
                f"Genera una descripción para la tarea: {task_data.get('title', '')}"
            )
            
            # Categorizar
            category, cat_info = self._call_llm(
                "Eres un experto en clasificación de tareas. Devuelve ÚNICAMENTE una categoría a partir de el tipo de tarea y la descrición. La categoría debe pertenecer a una de las siguientes opciones: Testing y Control de Calidad, Desarrollo Frontend, Desarrollo Backend, Desarrollo General , Diseño de Sistemas, Documentación, Base de Datos Seguridad, Infraestructura, Mantenimiento, Investigación, Supervisión, Riesgos Laborales, Limpieza, Otro.",
                f"Categoriza la tarea: {task_data.get('title', '')} - {description}"
            )
            
            # Estimar esfuerzo
            effort, eff_info = self._call_llm(
                "Eres un experto en estimación de tiempo para la ejecución de tareas. Calcula el tiempo en horas que toma ejecutar la tarea correspondiente, este dato debe estar entre 2 a 48 horas. Las tareas de desarrollo, control de calidad y testing toman al menos 8 horas, las tarewas de desarrollo de frontend, back end y desarrollo general toman 24 horas, las tarea de documentacion toma 4 horas, la tarea de base de datos toma 16 horas, la tarea de investigación toma 48 horas, supervisión y riesgos laborales toma 4 horas y otros toma 6 horas Devuelve ÚNICAMENTE un número de horas.",
                f"Estima las horas para: {task_data.get('title', '')} - {description}"
            )
            
            # Analizar riesgos
            risks, risk_info = self._call_llm(
                "Eres un experto en análisis de riesgos de ejecucion de tareas. Identifica los riesgos potenciales según la tarea y la descripción de la tarea. Genera una respuesta de máximo 200 palabras.",
                f"Analiza los riesgos de: {task_data.get('title', '')} - {description}"
            )
            
            # Generar mitigación
            mitigation, mit_info = self._call_llm(
                "Eres un experto en gestión de riesgos de un laboratorio de control de calidad de la industria farmacéutica. Genera un plan de mitigación para los riesgos potenciales según la tarea, su descripción y la descripción de los riesgos. Genera una respuesta de máximo 300 palabras.",
                f"Genera un plan de mitigación para los siguientes riesgos: {task_data.get('title', '')} - {description} - {risks}"
            )
            
            # Convertir categoría a valor interno usando el mapeo del enum
            category_clean = category.strip().lower()
            
            # Primero intentar buscar directamente en los valores del enum
            valid_values = TaskCategory.get_values()
            if category_clean in valid_values:
                category_value = category_clean
            else:
                # Si no se encuentra, intentar mapear desde nombres de visualización
                display_names = TaskCategory.get_display_names()
                reverse_mapping = {display_name.lower(): value for value, display_name in display_names.items()}
                category_value = reverse_mapping.get(category_clean, 'otro')
            
            # Actualizar datos de la tarea
            total_tokens = (
                desc_info['total_tokens'] +
                cat_info['total_tokens'] +
                eff_info['total_tokens'] +
                risk_info['total_tokens'] +
                mit_info['total_tokens']
            )
            
            total_cost = (
                desc_info['cost'] +
                cat_info['cost'] +
                eff_info['cost'] +
                risk_info['cost'] +
                mit_info['cost']
            )
            
            task_data.update({
                'description': description,
                'category': category_value,
                'effort': int(effort) if effort.isdigit() else 0,
                'risk_analysis': risks,
                'risk_mitigation': mitigation,
                'tokens_gastados': total_tokens,
                'costos': total_cost,
                'ai_processing': {
                    'description': desc_info,
                    'categorization': cat_info,
                    'effort_estimation': eff_info,
                    'risk_analysis': risk_info,
                    'mitigation': mit_info
                }
            })
            
            return task_data
            
        except Exception as e:
            raise Exception(f"Error al procesar la tarea: {str(e)}")

    def generate_description(self, title: str) -> Dict[str, Any]:
        """
        Genera una descripción detallada para una tarea
        
        Args:
            title: Título de la tarea
            
        Returns:
            Dict[str, Any]: Descripción generada y metadatos
        """
        try:
            description, token_info = self._call_llm(
                "Eres un experto en gestión de tareas de control de calidad. Genera una descripción profesional de máximo 200 palabras.",
                f"Genera una descripción para la tarea: {title}"
            )
            
            # Agregar logs para depuración
            print("\n=== Datos generados en generate_description ===")
            print(f"Token info: {token_info}")
            print(f"Tokens gastados: {token_info['total_tokens']}")
            print(f"Costos: {token_info['cost']}")
            
            response = {
                'success': True,
                'description': description,
                'total_tokens': token_info['total_tokens'],
                'cost': token_info['cost']
            }
            
            print(f"Response a devolver: {response}")
            print("===========================================\n")
            
            return response
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def categorize_task(self, title: str, description: str = '') -> Dict[str, Any]:
        """
        Categoriza una tarea usando IA
        
        Args:
            title: Título de la tarea
            description: Descripción de la tarea (opcional)
            
        Returns:
            Dict[str, Any]: Categoría generada y metadatos
        """
        try:
            category, token_info = self._call_llm(
                "Eres un experto en clasificación de tareas. Devuelve ÚNICAMENTE una categoría a partir de el tipo de tarea y la descripción. La categoría debe pertenecer a una de las siguientes opciones: Testing y Control de Calidad, Desarrollo Frontend, Desarrollo Backend, Desarrollo General , Diseño de Sistemas, Documentación, Base de Datos Seguridad, Infraestructura, Mantenimiento, Investigación, Supervisión, Riesgos Laborales, Limpieza, Otro.",
                f"Categoriza la tarea: {title} - {description}"
            )
            
            # Limpiar la categoría
            category = category.strip()
            
            # Usar el mapeo del enum para convertir nombres de visualización a valores internos
            display_names = TaskCategory.get_display_names()
            # Crear mapeo inverso: nombre de visualización -> valor interno
            reverse_mapping = {display_name: value for value, display_name in display_names.items()}
            
            # Convertir la categoría al valor interno
            select_value = reverse_mapping.get(category, 'otro')
            
            return {
                'success': True,
                'category': select_value,
                'total_tokens': token_info['total_tokens'],
                'cost': token_info['cost']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def estimate_effort(self, title: str, description: str = '', category: str = '') -> Dict[str, Any]:
        """
        Estima el esfuerzo necesario para una tarea
        
        Args:
            title: Título de la tarea
            description: Descripción de la tarea (opcional)
            category: Categoría de la tarea (opcional)
            
        Returns:
            Dict[str, Any]: Estimación de esfuerzo y metadatos
        """
        try:
            effort, token_info = self._call_llm(
                "Eres un experto en estimación de tiempo para la ejecución de tareas. Calcula el tiempo en horas que toma ejecutar la tarea correspondiente, este dato debe estar entre 2 a 48 horas. Las tareas de desarrollo, control de calidad y testing toman al menos 8 horas, las tarewas de desarrollo de frontend, back end y desarrollo general toman 24 horas, la tarea de documentacion toma 4 horas, la tarea de base de datos toma 16 horas, la tarea de investigación toma 48 horas, supervisión y riesgos laborales toma 4 horas y otros toma 6 horas Devuelve ÚNICAMENTE un número de horas.",
                f"Estima las horas para: {title} - {description} - {category}"
            )
            
            # Limpiar y convertir el esfuerzo a entero
            effort = effort.strip()
            try:
                effort = int(effort)
            except ValueError:
                effort = 0
            
            return {
                'success': True,
                'effort': effort,
                'total_tokens': token_info['total_tokens'],
                'cost': token_info['cost']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def analyze_risks(self, title: str, description: str = '', category: str = '') -> Dict[str, Any]:
        """
        Analiza los riesgos de una tarea
        
        Args:
            title: Título de la tarea
            description: Descripción de la tarea (opcional)
            category: Categoría de la tarea (opcional)
            
        Returns:
            Dict[str, Any]: Análisis de riesgos y metadatos
        """
        try:
            risks, token_info = self._call_llm(
                "Eres un experto en análisis de riesgos que se presentan en la ejecución de tareas. Identifica los riesgos potenciales según la tarea y la descripción de la tarea. Genera una respuesta de máximo 200 palabras.",
                f"Analiza los riesgos de: {title} - {description} - {category}"
            )
            
            return {
                'success': True,
                'risk_analysis': risks,
                'total_tokens': token_info['total_tokens'],
                'cost': token_info['cost']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def generate_mitigation(self, title: str, description: str = '', category: str = '', risk_analysis: str = '') -> Dict[str, Any]:
        """
        Genera un plan de mitigación para los riesgos de una tarea
        
        Args:
            title: Título de la tarea
            description: Descripción de la tarea (opcional)
            category: Categoría de la tarea (opcional)
            risk_analysis: Análisis de riesgos (opcional)
            
        Returns:
            Dict[str, Any]: Plan de mitigación y metadatos
        """
        try:
            mitigation, token_info = self._call_llm(
                "Eres un experto en gestión de riesgos en la ejecuciòn de tareas. Genera un plan de mitigación para los riesgos potenciales según la tarea, su descripción y la descripción de los riesgos. Genera una respuesta de máximo 200 palabras.",
                f"Genera un plan de mitigación para los siguientes riesgos: {title} - {description} - {category} - {risk_analysis}"
            )
            
            return {
                'success': True,
                'mitigation_plan': mitigation,
                'total_tokens': token_info['total_tokens'],
                'cost': token_info['cost']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            } 

    def generate_user_story(self, prompt: str) -> dict:
        """Genera una historia de usuario en español usando Azure OpenAI y devuelve un dict."""
        system_prompt = (
            "Eres un experto en gestión ágil de proyectos. Genera una historia de usuario en formato JSON con los campos: project, role, goal, reason, description, priority (baja, media, alta, bloqueante), story_points (1-8), effort_hours (decimal). Responde solo el JSON, sin explicaciones."
        )
        response_text, _ = self._call_llm(system_prompt, prompt)
        import json
        try:
            return json.loads(response_text)
        except Exception:
            # Si la respuesta no es JSON válido, intentar extraer el bloque JSON
            import re
            match = re.search(r'\{[\s\S]*\}', response_text)
            if match:
                return json.loads(match.group(0))
            raise ValueError(f"Respuesta de IA no es JSON válido: {response_text}")

    def generate_tasks(self, prompt: str) -> list:
        """Genera una lista de tareas en español usando Azure OpenAI y devuelve una lista de dicts."""
        system_prompt = (
            "Eres un experto en gestión de un laboratorio de control de calidad para la industria farmacéutica. "
            "Genera exactamente 5 tareas en formato JSON para una historia de usuario. "
            "Cada tarea debe tener un título concreto de máximo 30 palabras y una descripción de máximo 100 palabras. "
            "El formato debe ser: [{\"title\": \"Título de la tarea\", \"description\": \"Descripción de la tarea\"}, ...]. "
            "Responde solo el JSON, sin explicaciones."
        )
        response_text, _ = self._call_llm(system_prompt, prompt)
        import json
        try:
            tasks = json.loads(response_text)
            # Asegurar que devolvemos una lista
            if isinstance(tasks, list):
                return tasks
            else:
                # Si no es una lista, intentar convertir
                return [tasks] if isinstance(tasks, dict) else []
        except Exception as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Response text: {response_text}")
            # Si la respuesta no es JSON válido, intentar extraer el bloque JSON
            import re
            match = re.search(r'\[[\s\S]*\]', response_text)
            if match:
                try:
                    return json.loads(match.group(0))
                except:
                    pass
            # Fallback: crear tareas básicas
            return [
                {"title": "Tarea 1", "description": "Descripción de la tarea 1"},
                {"title": "Tarea 2", "description": "Descripción de la tarea 2"},
                {"title": "Tarea 3", "description": "Descripción de la tarea 3"},
                {"title": "Tarea 4", "description": "Descripción de la tarea 4"},
                {"title": "Tarea 5", "description": "Descripción de la tarea 5"}
            ] 