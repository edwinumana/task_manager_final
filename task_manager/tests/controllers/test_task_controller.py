"""
Unit tests for the TaskController class.
"""
import pytest
import json
from unittest.mock import patch, Mock
from app.controllers.task_controller import TaskController
from app.models.task import Task
from app.models.enums import TaskCategory
from app import create_app
from tests.test_config import TestConfig


class TestTaskController:
    """Test class for TaskController."""

    @pytest.fixture
    def task_controller(self):
        """Create a TaskController instance for testing."""
        return TaskController()

    @pytest.fixture
    def app(self):
        """Create a Flask app instance for testing."""
        app = create_app(TestConfig)
        return app

    @pytest.mark.unit
    def test_task_controller_initialization(self, task_controller):
        """Test TaskController initialization."""
        assert task_controller is not None
        assert hasattr(task_controller, 'task_manager')

    @pytest.mark.unit
    @patch('app.controllers.task_controller.TaskManager')
    def test_get_all_tasks_success(self, mock_task_manager_class, task_controller):
        """Test get_all_tasks method with successful response."""
        # Setup mock task manager
        mock_task_manager = Mock()
        mock_task_manager_class.return_value = mock_task_manager
        
        # Setup mock tasks - get_all_tasks returns dictionaries, not objects
        mock_tasks = [
            {
                'id': 1,
                'title': 'Task 1',
                'description': 'Description 1',
                'priority': 'alta',
                'status': 'pendiente',
                'category': 'desarrollo',
                'user_story_project': 'Test Project'
            },
            {
                'id': 2,
                'title': 'Task 2',
                'description': 'Description 2',
                'priority': 'media',
                'status': 'completada',
                'category': 'desarrollo',
                'user_story_project': 'Test Project'
            }
        ]
        
        mock_task_manager.get_all_tasks.return_value = mock_tasks
        
        # Create new controller to use mocked TaskManager
        controller = TaskController()
        
        # Call method
        result, status_code = controller.get_all_tasks()
        
        # Assertions
        assert status_code == 200
        assert result['success'] is True
        assert len(result['data']) == 2
        assert result['data'][0]['title'] == 'Task 1'
        assert result['data'][1]['title'] == 'Task 2'
        assert result['message'] == 'Tareas obtenidas exitosamente'

    @pytest.mark.unit
    @patch('app.controllers.task_controller.TaskManager')
    def test_get_all_tasks_exception(self, mock_task_manager_class, task_controller):
        """Test get_all_tasks method with exception."""
        # Setup mock task manager to raise exception
        mock_task_manager = Mock()
        mock_task_manager_class.return_value = mock_task_manager
        mock_task_manager.get_all_tasks.side_effect = Exception("Database error")
        
        # Create new controller to use mocked TaskManager
        controller = TaskController()
        
        # Call method
        result, status_code = controller.get_all_tasks()
        
        # Assertions
        assert status_code == 500
        assert result['success'] is False
        assert 'error' in result
        assert 'Database error' in result['error']

    @pytest.mark.unit
    @patch('app.controllers.task_controller.TaskManager')
    def test_get_task_by_id_success(self, mock_task_manager_class, task_controller):
        """Test get_task_by_id method with successful response."""
        # Setup mock task manager
        mock_task_manager = Mock()
        mock_task_manager_class.return_value = mock_task_manager
        mock_task = Mock()
        mock_task.to_dict.return_value = {
            'id': 1,
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': 'alta',
            'status': 'pendiente',
            'category': 'desarrollo'
        }
        mock_task_manager.get_task.return_value = mock_task
        
        # Create new controller to use mocked TaskManager
        controller = TaskController()
        
        # Call method
        result, status_code = controller.get_task_by_id(1)
        
        # Assertions
        assert status_code == 200
        assert result['success'] is True
        assert result['data']['id'] == 1
        assert result['data']['title'] == 'Test Task'
        assert result['message'] == 'Tarea obtenida exitosamente'

    @pytest.mark.unit
    @patch('app.controllers.task_controller.TaskManager')
    def test_get_task_by_id_not_found(self, mock_task_manager_class, task_controller):
        """Test get_task_by_id method with task not found."""
        # Setup mock task manager
        mock_task_manager = Mock()
        mock_task_manager_class.return_value = mock_task_manager
        mock_task_manager.get_task.return_value = None
        
        # Create new controller to use mocked TaskManager
        controller = TaskController()
        
        # Call method
        result, status_code = controller.get_task_by_id(999)
        
        # Assertions
        assert status_code == 404
        assert result['success'] is False
        assert result['error'] == 'Tarea no encontrada'

    @pytest.mark.unit
    def test_create_task_success(self, task_controller, app):
        """Test create_task method with successful response."""
        with app.test_request_context(
            json={
                'title': 'New Task',
                'description': 'Task description',
                'priority': 'alta',
                'status': 'pendiente'
            }
        ):
            with patch('app.controllers.task_controller.TaskManager') as mock_task_manager_class:
                # Setup mock task manager
                mock_task_manager = Mock()
                mock_task_manager_class.return_value = mock_task_manager
                mock_task = Mock()
                mock_task.to_dict.return_value = {
                    'id': 1,
                    'title': 'New Task',
                    'category': 'desarrollo'
                }
                mock_task_manager.create_task.return_value = mock_task
                
                # Create new controller to use mocked TaskManager
                controller = TaskController()
                
                # Call method
                result, status_code = controller.create_task()
                
                # Assertions
                assert status_code == 201
                assert result['success'] is True
                assert 'data' in result
                assert result['message'] == 'Tarea creada exitosamente'

    @pytest.mark.unit
    def test_create_task_no_data(self, task_controller, app):
        """Test create_task method with no data provided."""
        with app.test_request_context(json=None, content_type='application/json'):
            # Call method
            result, status_code = task_controller.create_task()
            
            # Assertions
            assert status_code == 400
            assert result['success'] is False
            assert result['error'] == 'No se proporcionaron datos'

    @pytest.mark.unit
    def test_create_task_no_title(self, task_controller, app):
        """Test create_task method with no title provided."""
        with app.test_request_context(
            json={
                'description': 'Task description',
                'priority': 'media'
            }
        ):
            # Call method
            result, status_code = task_controller.create_task()
            
            # Assertions
            assert status_code == 400
            assert result['success'] is False
            assert result['error'] == 'El título es requerido'

    @pytest.mark.unit
    def test_update_task_success(self, task_controller, app):
        """Test update_task method with successful response."""
        with app.test_request_context(
            json={
                'title': 'Updated Task',
                'description': 'Updated description',
                'priority': 'alta'
            }
        ):
            with patch('app.controllers.task_controller.TaskManager') as mock_task_manager_class:
                # Setup mock task manager
                mock_task_manager = Mock()
                mock_task_manager_class.return_value = mock_task_manager
                mock_task = Mock()
                mock_task.to_dict.return_value = {
                    'id': 1,
                    'title': 'Updated Task',
                    'category': 'desarrollo'
                }
                mock_task_manager.update_task.return_value = mock_task
                
                # Create new controller to use mocked TaskManager
                controller = TaskController()
                
                # Call method
                result, status_code = controller.update_task(1)
                
                # Assertions
                assert status_code == 200
                assert result['success'] is True
                assert 'data' in result
                assert result['message'] == 'Tarea actualizada exitosamente'

    @pytest.mark.unit
    def test_update_task_no_data(self, task_controller, app):
        """Test update_task method with no data provided."""
        with app.test_request_context(json=None, content_type='application/json'):
            # Call method
            result, status_code = task_controller.update_task(1)
            
            # Assertions
            assert status_code == 400
            assert result['success'] is False
            assert result['error'] == 'No se proporcionaron datos para actualizar'

    @pytest.mark.unit
    def test_update_task_invalid_priority(self, task_controller, app):
        """Test update_task method with invalid priority."""
        with app.test_request_context(
            json={
                'priority': 'invalid_priority'
            }
        ):
            # Call method
            result, status_code = task_controller.update_task(1)
            
            # Assertions
            assert status_code == 400
            assert result['success'] is False
            assert 'Prioridad inválida' in result['error']

    @pytest.mark.unit
    def test_update_task_invalid_status(self, task_controller, app):
        """Test update_task method with invalid status."""
        with app.test_request_context(
            json={
                'status': 'invalid_status'
            }
        ):
            # Call method
            result, status_code = task_controller.update_task(1)
            
            # Assertions
            assert status_code == 400
            assert result['success'] is False
            assert 'Estado inválido' in result['error']

    @pytest.mark.unit
    @patch('app.controllers.task_controller.TaskManager')
    def test_delete_task_success(self, mock_task_manager_class, task_controller):
        """Test delete_task method with successful response."""
        # Setup mock task manager
        mock_task_manager = Mock()
        mock_task_manager_class.return_value = mock_task_manager
        mock_task = Mock()
        mock_task_manager.get_task.return_value = mock_task
        mock_task_manager.delete_task.return_value = True
        
        # Create new controller to use mocked TaskManager
        controller = TaskController()
        
        # Call method
        result, status_code = controller.delete_task(1)
        
        # Assertions
        assert status_code == 200
        assert result['success'] is True
        assert result['message'] == 'Tarea eliminada exitosamente'

    @pytest.mark.unit
    @patch('app.controllers.task_controller.TaskManager')
    def test_delete_task_not_found(self, mock_task_manager_class, task_controller):
        """Test delete_task method with task not found."""
        # Setup mock task manager
        mock_task_manager = Mock()
        mock_task_manager_class.return_value = mock_task_manager
        mock_task_manager.get_task.return_value = None
        
        # Create new controller to use mocked TaskManager
        controller = TaskController()
        
        # Call method
        result, status_code = controller.delete_task(999)
        
        # Assertions
        assert status_code == 404
        assert result['success'] is False
        assert result['error'] == 'Tarea no encontrada'

    @pytest.mark.unit
    @patch('app.controllers.task_controller.TaskManager')
    def test_delete_task_failure(self, mock_task_manager_class, task_controller):
        """Test delete_task method with deletion failure."""
        # Setup mock task manager
        mock_task_manager = Mock()
        mock_task_manager_class.return_value = mock_task_manager
        mock_task = Mock()
        mock_task_manager.get_task.return_value = mock_task
        mock_task_manager.delete_task.return_value = False
        
        # Create new controller to use mocked TaskManager
        controller = TaskController()
        
        # Call method
        result, status_code = controller.delete_task(1)
        
        # Assertions
        assert status_code == 500
        assert result['success'] is False
        assert result['error'] == 'Error al eliminar la tarea'

    @pytest.mark.unit
    def test_generate_description_method_exists(self, task_controller):
        """Test that generate_description method exists."""
        assert hasattr(task_controller, 'generate_description')

    @pytest.mark.unit
    def test_estimate_effort_method_exists(self, task_controller):
        """Test that estimate_effort method exists."""
        assert hasattr(task_controller, 'estimate_effort')

    @pytest.mark.unit
    def test_analyze_risks_method_exists(self, task_controller):
        """Test that analyze_risks method exists."""
        assert hasattr(task_controller, 'analyze_risks')

    @pytest.mark.unit
    def test_generate_mitigation_method_exists(self, task_controller):
        """Test that generate_mitigation method exists."""
        assert hasattr(task_controller, 'generate_mitigation')

    @pytest.mark.unit
    def test_categorize_task_method_exists(self, task_controller):
        """Test that categorize_task method exists."""
        assert hasattr(task_controller, 'categorize_task')

    @pytest.mark.unit
    def test_enrich_task_method_exists(self, task_controller):
        """Test that enrich_task method exists."""
        assert hasattr(task_controller, 'enrich_task')

    @pytest.mark.unit
    def test_get_stats_method_exists(self, task_controller):
        """Test that get_stats method exists."""
        assert hasattr(task_controller, 'get_stats') 