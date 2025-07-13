"""
Unit tests for the Task model.
"""
import pytest
from datetime import datetime
from app.models.task import Task
from app.models.enums import TaskCategory


class TestTask:
    """Test class for Task model."""

    @pytest.mark.unit
    def test_task_initialization_with_defaults(self):
        """Test task initialization with default values."""
        task = Task()
        
        assert task.id is None
        assert task.title == ''
        assert task.description == ''
        assert task.priority == 'media'
        assert task.effort == 0
        assert task.status == 'pendiente'
        assert task.assigned_to == ''
        assert task.assigned_role == ''
        assert task.category == TaskCategory.OTRO.value
        assert task.risk_analysis == ''
        assert task.mitigation_plan == ''
        assert task.tokens_gastados == 0
        assert task.costos == 0.0
        assert task.created_at is not None
        assert task.updated_at is not None

    @pytest.mark.unit
    def test_task_initialization_with_values(self, sample_task_data):
        """Test task initialization with provided values."""
        task = Task(**sample_task_data)
        
        assert task.title == sample_task_data['title']
        assert task.description == sample_task_data['description']
        assert task.priority == sample_task_data['priority']
        assert task.effort == sample_task_data['effort']
        assert task.status == sample_task_data['status']
        assert task.assigned_to == sample_task_data['assigned_to']
        assert task.assigned_role == sample_task_data['assigned_role']
        assert task.category == sample_task_data['category']
        assert task.risk_analysis == sample_task_data['risk_analysis']
        assert task.mitigation_plan == sample_task_data['mitigation_plan']
        assert task.tokens_gastados == sample_task_data['tokens_gastados']
        assert task.costos == sample_task_data['costos']

    @pytest.mark.unit
    def test_task_priority_validation(self):
        """Test task priority validation."""
        # Valid priority
        task = Task(priority='alta')
        assert task.priority == 'alta'
        
        # Invalid priority defaults to 'media'
        task = Task(priority='invalid_priority')
        assert task.priority == 'media'

    @pytest.mark.unit
    def test_task_status_validation(self):
        """Test task status validation."""
        # Valid status
        task = Task(status='en_progreso')
        assert task.status == 'en_progreso'
        
        # Invalid status defaults to 'pendiente'
        task = Task(status='invalid_status')
        assert task.status == 'pendiente'

    @pytest.mark.unit
    def test_task_effort_conversion(self):
        """Test task effort field conversion."""
        # Valid integer
        task = Task(effort=8)
        assert task.effort == 8
        
        # String number
        task = Task(effort='16')
        assert task.effort == 16
        
        # Empty string
        task = Task(effort='')
        assert task.effort == 0
        
        # None value
        task = Task(effort=None)
        assert task.effort == 0
        
        # Invalid value
        task = Task(effort='not_a_number')
        assert task.effort == 0

    @pytest.mark.unit
    def test_task_category_validation(self):
        """Test task category validation."""
        # Valid category
        task = Task(category=TaskCategory.DESARROLLO.value)
        assert task.category == TaskCategory.DESARROLLO.value
        
        # Invalid category defaults to OTRO
        task = Task(category='invalid_category')
        assert task.category == TaskCategory.OTRO.value

    @pytest.mark.unit
    def test_task_to_dict(self, sample_task):
        """Test task to_dict method."""
        task_dict = sample_task.to_dict()
        
        assert isinstance(task_dict, dict)
        assert 'id' in task_dict
        assert 'title' in task_dict
        assert 'description' in task_dict
        assert 'priority' in task_dict
        assert 'effort' in task_dict
        assert 'status' in task_dict
        assert 'assigned_to' in task_dict
        assert 'assigned_role' in task_dict
        assert 'created_at' in task_dict
        assert 'updated_at' in task_dict
        assert 'category' in task_dict
        assert 'risk_analysis' in task_dict
        assert 'mitigation_plan' in task_dict
        assert 'tokens_gastados' in task_dict
        assert 'costos' in task_dict
        
        assert task_dict['title'] == sample_task.title
        assert task_dict['priority'] == sample_task.priority

    @pytest.mark.unit
    def test_task_from_dict(self, sample_task_data):
        """Test task from_dict class method."""
        task = Task.from_dict(sample_task_data)
        
        assert isinstance(task, Task)
        assert task.title == sample_task_data['title']
        assert task.description == sample_task_data['description']
        assert task.priority == sample_task_data['priority']
        assert task.effort == sample_task_data['effort']
        assert task.status == sample_task_data['status']

    @pytest.mark.unit
    def test_task_from_dict_with_missing_fields(self):
        """Test task from_dict with missing fields."""
        minimal_data = {'title': 'Minimal Task'}
        task = Task.from_dict(minimal_data)
        
        assert task.title == 'Minimal Task'
        assert task.description == ''
        assert task.priority == 'media'
        assert task.status == 'pendiente'
        assert task.effort == 0

    @pytest.mark.unit
    def test_task_from_dict_with_legacy_risk_mitigation(self):
        """Test task from_dict with legacy risk_mitigation field."""
        data = {
            'title': 'Legacy Task',
            'risk_mitigation': 'Legacy mitigation plan'
        }
        task = Task.from_dict(data)
        
        assert task.mitigation_plan == 'Legacy mitigation plan'

    @pytest.mark.unit
    def test_task_from_dict_token_conversion(self):
        """Test task from_dict with token and cost conversion."""
        data = {
            'title': 'Token Task',
            'tokens_gastados': '150',
            'costos': '0.15'
        }
        task = Task.from_dict(data)
        
        assert task.tokens_gastados == 150
        assert task.costos == 0.15
        
        # Test invalid values
        data_invalid = {
            'title': 'Invalid Token Task',
            'tokens_gastados': 'invalid',
            'costos': 'invalid'
        }
        task_invalid = Task.from_dict(data_invalid)
        
        assert task_invalid.tokens_gastados == 0
        assert task_invalid.costos == 0.0

    @pytest.mark.unit
    def test_task_update_method(self, sample_task):
        """Test task update method."""
        original_updated_at = sample_task.updated_at
        
        # Update valid fields
        sample_task.update(
            title='Updated Title',
            priority='alta',
            status='en_progreso',
            effort=16
        )
        
        assert sample_task.title == 'Updated Title'
        assert sample_task.priority == 'alta'
        assert sample_task.status == 'en_progreso'
        assert sample_task.effort == 16
        assert sample_task.updated_at != original_updated_at

    @pytest.mark.unit
    def test_task_update_with_invalid_values(self, sample_task):
        """Test task update method with invalid values."""
        original_priority = sample_task.priority
        original_status = sample_task.status
        original_category = sample_task.category
        
        # Try to update with invalid values
        sample_task.update(
            priority='invalid_priority',
            status='invalid_status',
            category='invalid_category'
        )
        
        # Values should remain unchanged
        assert sample_task.priority == original_priority
        assert sample_task.status == original_status
        assert sample_task.category == original_category

    @pytest.mark.unit
    def test_task_update_non_updatable_field(self, sample_task):
        """Test task update method with non-updatable field."""
        original_id = sample_task.id
        
        # Try to update non-updatable field
        sample_task.update(id=999)
        
        # ID should remain unchanged
        assert sample_task.id == original_id

    @pytest.mark.unit
    def test_task_repr(self, sample_task):
        """Test task __repr__ method."""
        repr_str = repr(sample_task)
        
        assert 'Task' in repr_str
        assert sample_task.title in repr_str

    @pytest.mark.unit
    def test_task_valid_priorities_constant(self):
        """Test VALID_PRIORITIES constant."""
        assert 'baja' in Task.VALID_PRIORITIES
        assert 'media' in Task.VALID_PRIORITIES
        assert 'alta' in Task.VALID_PRIORITIES
        assert 'bloqueante' in Task.VALID_PRIORITIES

    @pytest.mark.unit
    def test_task_valid_statuses_constant(self):
        """Test VALID_STATUSES constant."""
        assert 'pendiente' in Task.VALID_STATUSES
        assert 'en_progreso' in Task.VALID_STATUSES
        assert 'en_revision' in Task.VALID_STATUSES
        assert 'completada' in Task.VALID_STATUSES

    @pytest.mark.unit
    def test_task_datetime_fields(self):
        """Test that datetime fields are properly set."""
        task = Task()
        
        # created_at and updated_at should be set
        assert task.created_at is not None
        assert task.updated_at is not None
        
        # They should be ISO format strings
        datetime.fromisoformat(task.created_at.replace('Z', '+00:00') if task.created_at.endswith('Z') else task.created_at)
        datetime.fromisoformat(task.updated_at.replace('Z', '+00:00') if task.updated_at.endswith('Z') else task.updated_at)

    @pytest.mark.unit
    def test_task_custom_datetime(self):
        """Test task with custom datetime values."""
        custom_time = '2023-01-01T10:00:00'
        task = Task(created_at=custom_time, updated_at=custom_time)
        
        assert task.created_at == custom_time
        assert task.updated_at == custom_time 