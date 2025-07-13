"""
Integration tests for task routes.
"""
import pytest
import json
from unittest.mock import patch, Mock


class TestTaskRoutes:
    """Test class for task routes."""

    @pytest.mark.integration
    def test_task_index_route(self, client):
        """Test the main tasks index route."""
        response = client.get('/tasks/')
        
        assert response.status_code == 200
        assert b'text/html' in response.content_type.encode()

    @pytest.mark.integration
    def test_task_list_route(self, client):
        """Test the tasks list route."""
        response = client.get('/tasks/list')
        
        assert response.status_code == 200
        assert b'text/html' in response.content_type.encode()

    @pytest.mark.integration
    def test_task_stats_route(self, client):
        """Test the tasks stats route."""
        response = client.get('/tasks/stats')
        
        assert response.status_code == 200
        assert b'text/html' in response.content_type.encode()

    @pytest.mark.integration
    def test_task_view_route(self, client):
        """Test the task view route."""
        response = client.get('/tasks/1')
        
        assert response.status_code == 200
        assert b'text/html' in response.content_type.encode()

    @pytest.mark.integration
    @patch('app.controllers.task_controller.TaskController.get_all_tasks')
    def test_api_list_tasks_success(self, mock_get_all_tasks, client):
        """Test API endpoint to list all tasks."""
        # Mock successful response
        mock_get_all_tasks.return_value = ({
            'success': True,
            'tasks': [
                {'id': 1, 'title': 'Test Task 1'},
                {'id': 2, 'title': 'Test Task 2'}
            ],
            'total': 2
        }, 200)
        
        response = client.get('/tasks/api/list')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['tasks']) == 2

    @pytest.mark.integration
    @patch('app.controllers.task_controller.TaskController.get_task_by_id')
    def test_api_get_task_success(self, mock_get_task, client):
        """Test API endpoint to get a specific task."""
        # Mock successful response
        mock_get_task.return_value = ({
            'success': True,
            'data': {'id': 1, 'title': 'Test Task'}
        }, 200)
        
        response = client.get('/tasks/api/1')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['id'] == 1

    @pytest.mark.integration
    @patch('app.controllers.task_controller.TaskController.get_task_by_id')
    def test_api_get_task_not_found(self, mock_get_task, client):
        """Test API endpoint with non-existent task."""
        # Mock not found response
        mock_get_task.return_value = ({
            'success': False,
            'error': 'Tarea no encontrada'
        }, 404)
        
        response = client.get('/tasks/api/999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False

    @pytest.mark.integration
    @patch('app.controllers.task_controller.TaskController.create_task')
    def test_api_create_task_success(self, mock_create_task, client):
        """Test API endpoint to create a new task."""
        # Mock successful response
        mock_create_task.return_value = ({
            'success': True,
            'data': {'id': 1, 'title': 'New Task'},
            'message': 'Tarea creada exitosamente'
        }, 201)
        
        task_data = {
            'title': 'New Task',
            'description': 'Task description',
            'priority': 'media'
        }
        
        response = client.post(
            '/tasks/api',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['title'] == 'New Task'

    @pytest.mark.integration
    @patch('app.controllers.task_controller.TaskController.create_task')
    def test_api_create_task_invalid_data(self, mock_create_task, client):
        """Test API endpoint with invalid task data."""
        # Mock validation error response
        mock_create_task.return_value = ({
            'success': False,
            'error': 'El título es requerido'
        }, 400)
        
        task_data = {
            'description': 'Task without title'
        }
        
        response = client.post(
            '/tasks/api',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    @pytest.mark.integration
    @patch('app.controllers.task_controller.TaskController.update_task')
    def test_api_update_task_success(self, mock_update_task, client):
        """Test API endpoint to update a task."""
        # Mock successful response
        mock_update_task.return_value = ({
            'success': True,
            'data': {'id': 1, 'title': 'Updated Task'},
            'message': 'Tarea actualizada exitosamente'
        }, 200)
        
        update_data = {
            'title': 'Updated Task',
            'status': 'en_progreso'
        }
        
        response = client.put(
            '/tasks/api/1',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['title'] == 'Updated Task'

    @pytest.mark.integration
    @patch('app.controllers.task_controller.TaskController.delete_task')
    def test_api_delete_task_success(self, mock_delete_task, client):
        """Test API endpoint to delete a task."""
        # Mock successful response
        mock_delete_task.return_value = ({
            'success': True,
            'message': 'Tarea eliminada exitosamente'
        }, 200)
        
        response = client.delete('/tasks/api/1')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    @pytest.mark.integration
    @patch('app.controllers.task_controller.TaskController.get_stats')
    def test_api_get_stats(self, mock_get_stats, client):
        """Test API endpoint to get task statistics."""
        # Mock successful response
        mock_get_stats.return_value = ({
            'success': True,
            'stats': {
                'total': 10,
                'by_status': {'pendiente': 5, 'completada': 3, 'en_progreso': 2},
                'by_priority': {'alta': 3, 'media': 5, 'baja': 2}
            }
        }, 200)
        
        response = client.get('/tasks/api/stats')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'stats' in data

    @pytest.mark.integration
    def test_invalid_task_id_format(self, client):
        """Test API endpoints with invalid task ID format."""
        response = client.get('/tasks/api/invalid_id')
        
        # Should return 404 or handle gracefully
        assert response.status_code in [404, 400, 500]

    @pytest.mark.integration
    def test_api_post_without_content_type(self, client):
        """Test API POST endpoint without content type."""
        response = client.post('/tasks/api', data='invalid data')
        
        # Should handle missing content type gracefully
        assert response.status_code in [400, 415, 500]

    @pytest.mark.integration
    def test_api_post_invalid_json(self, client):
        """Test API POST endpoint with invalid JSON."""
        response = client.post(
            '/tasks/api',
            data='invalid json',
            content_type='application/json'
        )
        
        # Should handle invalid JSON gracefully
        assert response.status_code in [400, 422, 500]

    @pytest.mark.integration
    @patch('app.controllers.task_controller.TaskController.enrich_task')
    def test_api_enrich_task(self, mock_enrich_task, client):
        """Test API endpoint to enrich a task with AI."""
        # Mock successful response
        mock_enrich_task.return_value = ({
            'success': True,
            'message': 'Tarea enriquecida exitosamente'
        }, 200)
        
        response = client.post('/tasks/1/enrich')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    @pytest.mark.integration
    def test_root_redirect(self, client):
        """Test that root URL redirects to tasks."""
        response = client.get('/')
        
        # Should redirect to /tasks
        assert response.status_code in [301, 302]
        assert '/tasks' in response.location or '/tasks' in response.headers.get('Location', '')

    @pytest.mark.integration
    def test_tasks_routes_blueprint_registered(self, app):
        """Test that tasks blueprint is properly registered."""
        # Check that the blueprint routes are registered
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        
        assert '/tasks/' in rules
        assert '/tasks/api' in rules
        assert '/tasks/api/<int:task_id>' in rules or '/tasks/api/<task_id>' in rules 