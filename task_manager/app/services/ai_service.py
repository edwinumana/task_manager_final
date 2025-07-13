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
            # Obtener las credenciales del archivo .env
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            api_version = os.getenv("AZURE_OPENAI_API_VERSION")
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            
            # Verificar si estamos en modo testing
            is_testing = os.getenv("TESTING", "false").lower() == "true" or \
                        os.getenv("FLASK_ENV") == "testing"
            
            if is_testing:
                # En modo testing, usar valores por defecto
                print("🧪 Modo testing detectado - usando configuración mock para AIService")
                self.api_key = "test_key"
                self.api_version = "2023-12-01-preview"
                self.azure_endpoint = "https://test.openai.azure.com/"
                self.deployment_name = "test-deployment"
                self.is_testing = True
                return
            
            # Verificar que todas las credenciales estén presentes
            if not all([api_key, api_version, azure_endpoint]):
                raise ValueError("Faltan credenciales de Azure OpenAI en el archivo .env")
            
            # Configurar OpenAI para Azure (versión 0.28.1)
            openai.api_type = "azure"
            openai.api_key = api_key
            openai.api_base = azure_endpoint
            openai.api_version = api_version
            self.is_testing = False
            
            self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
            if not self.deployment_name:
                raise ValueError("Falta el nombre del deployment en el archivo .env")
            
            # Configuración del modelo
            self.temperature = float(os.getenv("TEMPERATURE", "0.5"))
            self.max_tokens = int(os.getenv("MAX_TOKENS", "500"))
            self.top_p = float(os.getenv("TOP_P", "0.2"))
            self.frequency_penalty = float(os.getenv("FREQUENCY_PENALTY", "0.0"))
            self.presence_penalty = float(os.getenv("PRESENCE_PENALTY", "0.0"))
            
            # Inicializar el codificador de tokens
            self.encoding = tiktoken.get_encoding("cl100k_base")
            
        except Exception as e:
            raise Exception(f"Error al inicializar el servicio de IA: {str(e)}")

    def _mock_llm_response(self, system_prompt: str, user_prompt: str) -> Tuple[str, Dict[str, Any]]:
        """
        Devuelve una respuesta mock para testing
        """
        mock_response = "Esta es una respuesta de prueba generada en modo testing."
        mock_stats = {
            'input_tokens': 50,
            'output_tokens': 20,
            'total_tokens': 70,
            'cost': 0.01
        }
        return mock_response, mock_stats

    def _call_llm(self, system_prompt: str, user_prompt: str) -> Tuple[str, Dict[str, Any]]:
        """
        Realiza una llamada al modelo de Azure OpenAI
        
        Args:
            system_prompt: Prompt del sistema que define el rol y comportamiento
            user_prompt: Prompt del usuario con la información específica
            
        Returns:
            Tuple[str, Dict[str, Any]]: (Respuesta del modelo, Información de tokens y costes)
        """
        try:
            # Si estamos en modo testing, devolver respuesta mock
            if getattr(self, 'is_testing', False):
                return self._mock_llm_response(system_prompt, user_prompt)
            
            # Contar tokens de entrada
            input_tokens = self.count_tokens(system_prompt) + self.count_tokens(user_prompt)
            
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
                presence_penalty=self.presence_penalty
            )
            
            # Obtener respuesta y contar tokens de salida
            response_text = response.choices[0].message.content.strip()
            output_tokens = self.count_tokens(response_text)
            
            # Calcular coste
            total_cost = self.calculate_cost(input_tokens, output_tokens)
            
            # Crear diccionario con información de tokens y costes
            token_info = {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
                "cost": total_cost
            }
            
            # Agregar logs para depuración
            print("\n=== Información de Tokens y Costos ===")
            print(f"Token info: {token_info}")
            print("=====================================\n")
            
            return response_text, token_info
            
        except Exception as e:
            error_message = str(e)
            
            # Manejar errores específicos de Azure OpenAI
            if "429" in error_message or "Too Many Requests" in error_message:
                raise Exception("Se ha excedido el límite de solicitudes a Azure OpenAI. Por favor, espera un momento antes de intentar nuevamente.")
            elif "authentication" in error_message.lower():
                raise Exception("Error de autenticación con Azure OpenAI. Verifica tus credenciales.")
            elif "api" in error_message.lower():
                raise Exception(f"Error en la API de Azure OpenAI: {error_message}")
            elif "timeout" in error_message.lower():
                raise Exception("La solicitud a Azure OpenAI ha excedido el tiempo de espera. Intenta nuevamente.")
            elif "quota" in error_message.lower():
                raise Exception("Se ha excedido la cuota de Azure OpenAI. Verifica tu plan de suscripción.")
            else:
                raise Exception(f"Error al llamar al modelo: {error_message}")

    def count_tokens(self, text: str) -> int:
        """Cuenta el número de tokens en un texto"""
        return len(self.encoding.encode(text))

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calcula el coste de una ejecución basado en los tokens"""
        INPUT_COST_PER_1K = 0.01
        OUTPUT_COST_PER_1K = 0.03
        input_cost = (input_tokens / 1000) * INPUT_COST_PER_1K
        output_cost = (output_tokens / 1000) * OUTPUT_COST_PER_1K
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
            category_clean = category.strip()
            display_names = TaskCategory.get_display_names()
            reverse_mapping = {display_name: value for value, display_name in display_names.items()}
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