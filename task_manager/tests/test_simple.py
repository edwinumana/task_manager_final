"""
Test simple para verificar que pytest funciona.
"""
import pytest
import os
import sys

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_basic_python():
    """Test básico para verificar que Python funciona."""
    assert 1 + 1 == 2
    assert "hello" == "hello"
    assert [1, 2, 3] == [1, 2, 3]

def test_imports_basic():
    """Test para verificar que las importaciones básicas funcionan."""
    # Test imports sin AIService
    from app.models.task import Task
    from app.models.enums import TaskCategory
    
    # Verificar que las clases existen
    assert Task is not None
    assert TaskCategory is not None
    
    # Test creación básica de Task
    task = Task(title="Test Task")
    assert task.title == "Test Task"
    assert task.priority == "media"  # valor por defecto

def test_task_category_enum():
    """Test para verificar que el enum TaskCategory funciona."""
    from app.models.enums import TaskCategory
    
    # Verificar valores del enum
    assert TaskCategory.DESARROLLO.value == "desarrollo"
    assert TaskCategory.TESTING.value == "testing"
    assert TaskCategory.OTRO.value == "otro"
    
    # Verificar get_values
    values = TaskCategory.get_values()
    assert "desarrollo" in values
    assert "testing" in values
    assert len(values) == 15

@pytest.mark.unit
def test_task_model_basic():
    """Test básico del modelo Task."""
    from app.models.task import Task
    from app.models.enums import TaskCategory
    
    # Test inicialización con valores por defecto
    task = Task()
    assert task.title == ''
    assert task.priority == 'media'
    assert task.status == 'pendiente'
    assert task.effort == 0
    
    # Test inicialización con valores específicos
    task_data = {
        'title': 'Tarea de prueba',
        'description': 'Descripción de prueba',
        'priority': 'alta',
        'effort': 8,
        'category': TaskCategory.DESARROLLO.value
    }
    
    task = Task(**task_data)
    assert task.title == 'Tarea de prueba'
    assert task.priority == 'alta'
    assert task.effort == 8
    assert task.category == TaskCategory.DESARROLLO.value

@pytest.mark.unit
def test_task_validation():
    """Test validaciones del modelo Task."""
    from app.models.task import Task
    
    # Test validación de prioridad inválida
    task = Task(priority='invalida')
    assert task.priority == 'media'  # debe usar valor por defecto
    
    # Test validación de estado inválido
    task = Task(status='invalido')
    assert task.status == 'pendiente'  # debe usar valor por defecto
    
    # Test conversión de effort
    task = Task(effort='8')
    assert task.effort == 8
    assert isinstance(task.effort, int)

@pytest.mark.unit  
def test_task_methods():
    """Test métodos del modelo Task."""
    from app.models.task import Task
    
    task_data = {
        'title': 'Test Task',
        'description': 'Test Description',
        'priority': 'alta'
    }
    
    # Test to_dict
    task = Task(**task_data)
    task_dict = task.to_dict()
    
    assert isinstance(task_dict, dict)
    assert task_dict['title'] == 'Test Task'
    assert task_dict['priority'] == 'alta'
    assert 'created_at' in task_dict
    
    # Test from_dict
    new_task = Task.from_dict(task_dict)
    assert new_task.title == task.title
    assert new_task.priority == task.priority
    
    # Test update
    task.update(title='Updated Title', effort=16)
    assert task.title == 'Updated Title'
    assert task.effort == 16 