"""
Unit tests for the TaskManager utility class.
"""
import pytest
from unittest.mock import patch, Mock, MagicMock
from app.utils.task_manager import TaskManager
from app.models.task import Task
from app.models.task_db import TaskDB


class TestTaskManager:
    """Test class for TaskManager utility."""

    @pytest.mark.unit
    def test_task_manager_initialization(self):
        """Test TaskManager initialization."""
        manager = TaskManager()
        
        assert manager is not None
        assert hasattr(manager, 'use_database')
        assert manager.use_database is True

    @pytest.mark.unit
    def test_task_manager_initialization_no_database(self):
        """Test TaskManager initialization without database."""
        manager = TaskManager(use_database=False)
        
        assert manager.use_database is False

    @pytest.mark.unit
    @patch('app.utils.task_manager.get_db_session')
    def test_get_next_id_with_database(self, mock_get_session):
        """Test get_next_id method with database."""
        # Setup mock session
        mock_session = Mock()
        mock_get_session.return_value = mock_session
        
        # Mock query result
        mock_session.query.return_value.order_by.return_value.first.return_value = (5,)
        
        manager = TaskManager(use_database=True)
        next_id = manager.get_next_id()
        
        assert next_id == 6
        mock_session.close.assert_called_once()

    @pytest.mark.unit
    @patch('app.utils.task_manager.get_db_session')
    def test_get_next_id_empty_database(self, mock_get_session):
        """Test get_next_id method with empty database."""
        # Setup mock session
        mock_session = Mock()
        mock_get_session.return_value = mock_session
        
        # Mock empty query result
        mock_session.query.return_value.order_by.return_value.first.return_value = None
        
        manager = TaskManager(use_database=True)
        next_id = manager.get_next_id()
        
        assert next_id == 1
        mock_session.close.assert_called_once()

    @pytest.mark.unit
    def test_get_next_id_no_database(self):
        """Test get_next_id method without database."""
        manager = TaskManager(use_database=False)
        next_id = manager.get_next_id()
        
        assert next_id == 1

    @pytest.mark.unit
    @patch('app.utils.task_manager.get_db_session')
    def test_create_task_with_database(self, mock_get_session, sample_task_data):
        """Test create_task method with database."""
        # Setup mock session
        mock_session = Mock()
        mock_get_session.return_value = mock_session
        
        # Mock TaskDB instance
        mock_task_db = Mock()
        mock_task_db.to_dict.return_value = {**sample_task_data, 'id': 1}
        
        with patch('app.utils.task_manager.TaskDB') as mock_task_db_class:
            mock_task_db_class.from_dict.return_value = mock_task_db
            
            manager = TaskManager(use_database=True)
            result = manager.create_task(sample_task_data)
            
            assert isinstance(result, Task)
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()
            mock_session.close.assert_called_once()

    @pytest.mark.unit
    def test_create_task_no_database(self, sample_task_data):
        """Test create_task method without database."""
        manager = TaskManager(use_database=False)
        
        with pytest.raises(Exception) as exc_info:
            manager.create_task(sample_task_data)
        
        assert "Modo JSON no disponible" in str(exc_info.value)

    @pytest.mark.unit
    @patch('app.utils.task_manager.get_db_session')
    def test_create_task_database_error(self, mock_get_session, sample_task_data):
        """Test create_task method with database error."""
        # Setup mock session that raises exception
        mock_session = Mock()
        mock_get_session.return_value = mock_session
        mock_session.commit.side_effect = Exception("Database error")
        
        with patch('app.utils.task_manager.TaskDB'):
            manager = TaskManager(use_database=True)
            
            with pytest.raises(Exception):
                manager.create_task(sample_task_data)
            
            mock_session.rollback.assert_called_once()
            mock_session.close.assert_called_once()

    @pytest.mark.unit
    @patch('app.utils.task_manager.get_db_session')
    def test_get_all_tasks_with_database(self, mock_get_session):
        """Test get_all_tasks method with database."""
        # Setup mock session
        mock_session = Mock()
        mock_get_session.return_value = mock_session
        
        # Mock query result
        mock_tasks = [Mock(), Mock()]
        for i, task in enumerate(mock_tasks):
            task.to_dict.return_value = {'id': i+1, 'title': f'Task {i+1}'}
            task.user_story = None
        
        mock_session.query.return_value.outerjoin.return_value.all.return_value = mock_tasks
        
        manager = TaskManager(use_database=True)
        result = manager.get_all_tasks()
        
        assert len(result) == 2
        assert all(isinstance(task, dict) for task in result)
        mock_session.close.assert_called_once()

    @pytest.mark.unit
    @patch('app.utils.task_manager.get_db_session')
    def test_get_task_with_database(self, mock_get_session):
        """Test get_task method with database."""
        # Setup mock session
        mock_session = Mock()
        mock_get_session.return_value = mock_session
        
        # Mock query result
        mock_task_db = Mock()
        mock_task_db.to_dict.return_value = {'id': 1, 'title': 'Test Task'}
        mock_session.query.return_value.filter.return_value.first.return_value = mock_task_db
        
        manager = TaskManager(use_database=True)
        result = manager.get_task(1)
        
        assert isinstance(result, Task)
        mock_session.close.assert_called_once()

    @pytest.mark.unit
    @patch('app.utils.task_manager.get_db_session')
    def test_get_task_not_found(self, mock_get_session):
        """Test get_task method with non-existent task."""
        # Setup mock session
        mock_session = Mock()
        mock_get_session.return_value = mock_session
        
        # Mock empty query result
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        manager = TaskManager(use_database=True)
        result = manager.get_task(999)
        
        assert result is None
        mock_session.close.assert_called_once()

    @pytest.mark.unit
    @patch('app.utils.task_manager.get_db_session')
    def test_update_task_with_database(self, mock_get_session):
        """Test update_task method with database."""
        # Setup mock session
        mock_session = Mock()
        mock_get_session.return_value = mock_session
        
        # Mock existing task
        mock_task_db = Mock()
        mock_task_db.to_dict.return_value = {'id': 1, 'title': 'Updated Task'}
        mock_session.query.return_value.filter.return_value.first.return_value = mock_task_db
        
        manager = TaskManager(use_database=True)
        result = manager.update_task(1, {'title': 'Updated Task'})
        
        assert isinstance(result, Task)
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

    @pytest.mark.unit
    @patch('app.utils.task_manager.get_db_session')
    def test_update_task_not_found(self, mock_get_session):
        """Test update_task method with non-existent task."""
        # Setup mock session
        mock_session = Mock()
        mock_get_session.return_value = mock_session
        
        # Mock empty query result
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        manager = TaskManager(use_database=True)
        result = manager.update_task(999, {'title': 'Updated Task'})
        
        assert result is None
        mock_session.close.assert_called_once()

    @pytest.mark.unit
    @patch('app.utils.task_manager.get_db_session')
    def test_delete_task_with_database(self, mock_get_session):
        """Test delete_task method with database."""
        # Setup mock session
        mock_session = Mock()
        mock_get_session.return_value = mock_session
        
        # Mock existing task
        mock_task_db = Mock()
        mock_session.query.return_value.filter.return_value.first.return_value = mock_task_db
        
        manager = TaskManager(use_database=True)
        result = manager.delete_task(1)
        
        assert result is True
        mock_session.delete.assert_called_once_with(mock_task_db)
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

    @pytest.mark.unit
    @patch('app.utils.task_manager.get_db_session')
    def test_delete_task_not_found(self, mock_get_session):
        """Test delete_task method with non-existent task."""
        # Setup mock session
        mock_session = Mock()
        mock_get_session.return_value = mock_session
        
        # Mock empty query result
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        manager = TaskManager(use_database=True)
        result = manager.delete_task(999)
        
        assert result is False
        mock_session.close.assert_called_once()

    @pytest.mark.unit
    @patch('app.utils.task_manager.get_db_session')
    def test_get_task_with_user_story(self, mock_get_session):
        """Test get_task_with_user_story method."""
        # Setup mock session
        mock_session = Mock()
        mock_get_session.return_value = mock_session
        
        # Mock query result with user story
        mock_task_db = Mock()
        mock_user_story = Mock()
        mock_user_story.project = "Test Project"
        mock_task_db.user_story = mock_user_story
        mock_task_db.to_dict.return_value = {'id': 1, 'title': 'Test Task'}
        
        mock_session.query.return_value.outerjoin.return_value.filter.return_value.first.return_value = mock_task_db
        
        manager = TaskManager(use_database=True)
        result = manager.get_task_with_user_story(1)
        
        assert isinstance(result, dict)
        assert 'user_story_project' in result
        mock_session.close.assert_called_once()

    @pytest.mark.unit
    @patch('app.utils.task_manager.get_db_session')
    def test_database_error_handling(self, mock_get_session):
        """Test database error handling."""
        # Setup mock session that raises exception
        mock_session = Mock()
        mock_get_session.side_effect = Exception("Database connection error")
        
        manager = TaskManager(use_database=True)
        
        # Should handle the error gracefully
        with pytest.raises(Exception):
            manager.get_all_tasks()

    @pytest.mark.unit
    def test_task_manager_method_signatures(self):
        """Test that TaskManager has all expected methods."""
        manager = TaskManager()
        
        # Check that all expected methods exist
        expected_methods = [
            'get_next_id',
            'create_task',
            'get_all_tasks',
            'get_task',
            'update_task',
            'delete_task',
            'get_task_with_user_story'
        ]
        
        for method_name in expected_methods:
            assert hasattr(manager, method_name)
            assert callable(getattr(manager, method_name)) 