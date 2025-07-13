"""
Tests aislados para los modelos sin dependencias de la aplicación completa.
"""
import pytest
import sys
import os
from datetime import datetime

# Agregar el directorio padre al path para importaciones directas
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_task_category_enum_isolated():
    """Test del enum TaskCategory de forma aislada."""
    # Importación directa sin pasar por app/__init__.py
    from app.models.enums import TaskCategory
    
    # Verificar valores del enum
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
    assert "frontend" in values

def test_task_model_isolated():
    """Test del modelo Task de forma aislada."""
    # Importación directa
    from app.models.task import Task
    from app.models.enums import TaskCategory
    
    # Test inicialización por defecto
    task = Task()
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
    
    # Verificar que las fechas se establecen
    assert task.created_at is not None
    assert task.updated_at is not None

def test_task_model_with_data():
    """Test del modelo Task con datos específicos."""
    from app.models.task import Task
    from app.models.enums import TaskCategory
    
    task_data = {
        'title': 'Tarea de prueba',
        'description': 'Descripción de la tarea de prueba',
        'priority': 'alta',
        'effort': 16,
        'status': 'en_progreso',
        'assigned_to': 'Edwin Umaña',
        'assigned_role': 'Desarrollador',
        'category': TaskCategory.DESARROLLO.value,
        'risk_analysis': 'Riesgo bajo',
        'mitigation_plan': 'Plan de mitigación estándar',
        'tokens_gastados': 150,
        'costos': 0.15
    }
    
    task = Task(**task_data)
    
    # Verificar todos los campos
    assert task.title == 'Tarea de prueba'
    assert task.description == 'Descripción de la tarea de prueba'
    assert task.priority == 'alta'
    assert task.effort == 16
    assert task.status == 'en_progreso'
    assert task.assigned_to == 'Edwin Umaña'
    assert task.assigned_role == 'Desarrollador'
    assert task.category == TaskCategory.DESARROLLO.value
    assert task.risk_analysis == 'Riesgo bajo'
    assert task.mitigation_plan == 'Plan de mitigación estándar'
    assert task.tokens_gastados == 150
    assert task.costos == 0.15

def test_task_validation_priority():
    """Test validación de prioridad en Task."""
    from app.models.task import Task
    
    # Prioridades válidas
    valid_priorities = ['baja', 'media', 'alta', 'bloqueante']
    
    for priority in valid_priorities:
        task = Task(priority=priority)
        assert task.priority == priority
    
    # Prioridad inválida debe usar 'media' por defecto
    task = Task(priority='prioridad_invalida')
    assert task.priority == 'media'

def test_task_validation_status():
    """Test validación de estado en Task."""
    from app.models.task import Task
    
    # Estados válidos
    valid_statuses = ['pendiente', 'en_progreso', 'en_revision', 'completada']
    
    for status in valid_statuses:
        task = Task(status=status)
        assert task.status == status
    
    # Estado inválido debe usar 'pendiente' por defecto
    task = Task(status='estado_invalido')
    assert task.status == 'pendiente'

def test_task_effort_conversion():
    """Test conversión del campo effort."""
    from app.models.task import Task
    
    # Número entero
    task = Task(effort=8)
    assert task.effort == 8
    assert isinstance(task.effort, int)
    
    # String que es número
    task = Task(effort='16')
    assert task.effort == 16
    assert isinstance(task.effort, int)
    
    # String vacío
    task = Task(effort='')
    assert task.effort == 0
    
    # None
    task = Task(effort=None)
    assert task.effort == 0
    
    # Valor inválido
    task = Task(effort='no_es_numero')
    assert task.effort == 0

def test_task_to_dict():
    """Test método to_dict de Task."""
    from app.models.task import Task
    from app.models.enums import TaskCategory
    
    task = Task(
        title='Test Task',
        description='Test Description',
        priority='alta',
        effort=8,
        category=TaskCategory.TESTING.value
    )
    
    task_dict = task.to_dict()
    
    # Verificar que es un diccionario
    assert isinstance(task_dict, dict)
    
    # Verificar campos clave
    assert task_dict['title'] == 'Test Task'
    assert task_dict['description'] == 'Test Description'
    assert task_dict['priority'] == 'alta'
    assert task_dict['effort'] == 8
    assert task_dict['category'] == TaskCategory.TESTING.value
    
    # Verificar que contiene todos los campos esperados
    expected_fields = [
        'id', 'title', 'description', 'priority', 'effort', 'status',
        'assigned_to', 'assigned_role', 'created_at', 'updated_at',
        'category', 'risk_analysis', 'mitigation_plan', 'tokens_gastados', 'costos'
    ]
    
    for field in expected_fields:
        assert field in task_dict

def test_task_from_dict():
    """Test método from_dict de Task."""
    from app.models.task import Task
    from app.models.enums import TaskCategory
    
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
    
    task = Task.from_dict(task_data)
    
    # Verificar que es una instancia de Task
    assert isinstance(task, Task)
    
    # Verificar campos
    assert task.id == 1
    assert task.title == 'Tarea desde dict'
    assert task.description == 'Descripción desde dict'
    assert task.priority == 'media'
    assert task.effort == 12
    assert task.status == 'pendiente'
    assert task.category == TaskCategory.BACKEND.value
    assert task.tokens_gastados == 100
    assert task.costos == 0.10

def test_task_from_dict_minimal():
    """Test from_dict con datos mínimos."""
    from app.models.task import Task
    
    minimal_data = {'title': 'Tarea mínima'}
    task = Task.from_dict(minimal_data)
    
    assert task.title == 'Tarea mínima'
    assert task.description == ''
    assert task.priority == 'media'
    assert task.status == 'pendiente'
    assert task.effort == 0

def test_task_update_method():
    """Test método update de Task."""
    from app.models.task import Task
    
    task = Task(title='Título original', priority='baja', effort=4)
    original_updated_at = task.updated_at
    
    # Actualizar campos
    task.update(
        title='Título actualizado',
        priority='alta',
        effort=8,
        status='en_progreso'
    )
    
    # Verificar cambios
    assert task.title == 'Título actualizado'
    assert task.priority == 'alta'
    assert task.effort == 8
    assert task.status == 'en_progreso'
    
    # Verificar que updated_at cambió
    assert task.updated_at != original_updated_at

def test_task_update_invalid_values():
    """Test update con valores inválidos."""
    from app.models.task import Task
    
    task = Task(priority='media', status='pendiente')
    original_priority = task.priority
    original_status = task.status
    
    # Intentar actualizar con valores inválidos
    task.update(
        priority='prioridad_invalida',
        status='estado_invalido'
    )
    
    # Los valores deben permanecer sin cambios
    assert task.priority == original_priority
    assert task.status == original_status

def test_task_constants():
    """Test constantes de validación en Task."""
    from app.models.task import Task
    
    # Verificar VALID_PRIORITIES
    expected_priorities = ['baja', 'media', 'alta', 'bloqueante']
    assert Task.VALID_PRIORITIES == expected_priorities
    
    # Verificar VALID_STATUSES
    expected_statuses = ['pendiente', 'en_progreso', 'en_revision', 'completada']
    assert Task.VALID_STATUSES == expected_statuses

def test_task_repr():
    """Test método __repr__ de Task."""
    from app.models.task import Task
    
    task = Task(id=1, title='Tarea de prueba')
    repr_str = repr(task)
    
    assert 'Task' in repr_str
    assert '1' in repr_str
    assert 'Tarea de prueba' in repr_str

def test_task_category_validation():
    """Test validación de categoría en Task."""
    from app.models.task import Task
    from app.models.enums import TaskCategory
    
    # Categoría válida
    task = Task(category=TaskCategory.DESARROLLO.value)
    assert task.category == TaskCategory.DESARROLLO.value
    
    # Categoría inválida debe usar OTRO por defecto
    task = Task(category='categoria_invalida')
    assert task.category == TaskCategory.OTRO.value

def test_all_task_categories():
    """Test todas las categorías de Task."""
    from app.models.enums import TaskCategory
    
    # Verificar que todas las categorías esperadas existen
    expected_categories = [
        'testing', 'frontend', 'backend', 'desarrollo', 'diseño',
        'documentacion', 'base_de_datos', 'seguridad', 'infraestructura',
        'mantenimiento', 'investigacion', 'supervision', 'riesgos_laborales',
        'limpieza', 'otro'
    ]
    
    actual_values = TaskCategory.get_values()
    
    for expected in expected_categories:
        assert expected in actual_values
    
    assert len(actual_values) == len(expected_categories) 