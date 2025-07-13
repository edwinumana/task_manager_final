"""
Unit tests for the TaskDB model.
"""
import pytest
from sqlalchemy.exc import IntegrityError
from app.models.task_db import TaskDB, StatusEnum, PriorityEnum
from app.models.enums import TaskCategory
from tests.conftest import create_test_task_db, create_test_user_story


class TestTaskDB:
    """Test class for TaskDB model."""

    @pytest.mark.unit
    @pytest.mark.database
    def test_task_db_creation(self, database_session, sample_task_db_data):
        """Test TaskDB creation with valid data."""
        task_db = TaskDB(**sample_task_db_data)
        database_session.add(task_db)
        database_session.commit()
        database_session.refresh(task_db)
        
        assert task_db.id is not None
        assert task_db.title == sample_task_db_data['title']
        assert task_db.description == sample_task_db_data['description']
        assert task_db.priority == sample_task_db_data['priority']
        assert task_db.status == sample_task_db_data['status']
        assert task_db.effort == sample_task_db_data['effort']
        assert task_db.assigned_to == sample_task_db_data['assigned_to']
        assert task_db.assigned_role == sample_task_db_data['assigned_role']
        assert task_db.category == sample_task_db_data['category']
        assert task_db.created_at is not None
        assert task_db.updated_at is not None

    @pytest.mark.unit
    @pytest.mark.database
    def test_task_db_default_values(self, database_session):
        """Test TaskDB with default values."""
        task_db = TaskDB(title="Test Task")
        database_session.add(task_db)
        database_session.commit()
        database_session.refresh(task_db)
        
        assert task_db.title == "Test Task"
        assert task_db.priority == PriorityEnum.MEDIA
        assert task_db.status == StatusEnum.PENDIENTE
        assert task_db.effort == 0
        assert task_db.category == TaskCategory.OTRO
        assert task_db.tokens_gastados == 0
        assert task_db.costos == 0.0

    @pytest.mark.unit
    @pytest.mark.database
    def test_task_db_title_required(self, database_session):
        """Test that title is required for TaskDB."""
        task_db = TaskDB()  # No title provided
        database_session.add(task_db)
        
        with pytest.raises(IntegrityError):
            database_session.commit()

    @pytest.mark.unit
    @pytest.mark.database
    def test_task_db_enum_fields(self, database_session):
        """Test TaskDB enum fields."""
        task_db = TaskDB(
            title="Enum Test Task",
            priority=PriorityEnum.ALTA,
            status=StatusEnum.EN_PROGRESO,
            category=TaskCategory.TESTING
        )
        database_session.add(task_db)
        database_session.commit()
        database_session.refresh(task_db)
        
        assert task_db.priority == PriorityEnum.ALTA
        assert task_db.status == StatusEnum.EN_PROGRESO
        assert task_db.category == TaskCategory.TESTING

    @pytest.mark.unit
    @pytest.mark.database
    def test_task_db_relationship_with_user_story(self, database_session):
        """Test TaskDB relationship with UserStory."""
        # Create a user story first
        user_story = create_test_user_story(database_session)
        
        # Create a task linked to the user story
        task_db = create_test_task_db(
            database_session,
            title="Related Task",
            user_story_id=user_story.id
        )
        
        assert task_db.user_story_id == user_story.id
        assert task_db.user_story == user_story
        assert task_db in user_story.tasks

    @pytest.mark.unit
    @pytest.mark.database
    def test_task_db_repr(self, database_session):
        """Test TaskDB __repr__ method."""
        task_db = create_test_task_db(database_session, title="Repr Test Task")
        
        repr_str = repr(task_db)
        assert 'TaskDB' in repr_str
        assert str(task_db.id) in repr_str
        assert 'Repr Test Task' in repr_str
        assert task_db.status.value in repr_str

    @pytest.mark.unit
    @pytest.mark.database
    def test_task_db_to_dict_method(self, database_session):
        """Test TaskDB to_dict method if it exists."""
        task_db = create_test_task_db(database_session)
        
        # Check if to_dict method exists and works
        if hasattr(task_db, 'to_dict'):
            task_dict = task_db.to_dict()
            assert isinstance(task_dict, dict)
            assert 'id' in task_dict
            assert 'title' in task_dict
            assert task_dict['title'] == task_db.title

    @pytest.mark.unit
    @pytest.mark.database
    def test_task_db_from_dict_method(self, database_session, sample_task_data):
        """Test TaskDB from_dict method if it exists."""
        # Check if from_dict class method exists
        if hasattr(TaskDB, 'from_dict'):
            task_db = TaskDB.from_dict(sample_task_data)
            database_session.add(task_db)
            database_session.commit()
            database_session.refresh(task_db)
            
            assert task_db.title == sample_task_data['title']
            assert task_db.description == sample_task_data['description']

    @pytest.mark.unit
    @pytest.mark.database
    def test_task_db_query_by_status(self, database_session):
        """Test querying TaskDB by status."""
        # Create tasks with different statuses
        task1 = create_test_task_db(
            database_session,
            title="Pending Task",
            status=StatusEnum.PENDIENTE
        )
        task2 = create_test_task_db(
            database_session,
            title="In Progress Task",
            status=StatusEnum.EN_PROGRESO
        )
        
        # Query by status
        pending_tasks = database_session.query(TaskDB).filter(
            TaskDB.status == StatusEnum.PENDIENTE
        ).all()
        
        assert len(pending_tasks) >= 1
        assert task1 in pending_tasks
        assert task2 not in pending_tasks

    @pytest.mark.unit
    @pytest.mark.database
    def test_task_db_query_by_priority(self, database_session):
        """Test querying TaskDB by priority."""
        # Create tasks with different priorities
        task1 = create_test_task_db(
            database_session,
            title="High Priority Task",
            priority=PriorityEnum.ALTA
        )
        task2 = create_test_task_db(
            database_session,
            title="Medium Priority Task",
            priority=PriorityEnum.MEDIA
        )
        
        # Query by priority
        high_priority_tasks = database_session.query(TaskDB).filter(
            TaskDB.priority == PriorityEnum.ALTA
        ).all()
        
        assert len(high_priority_tasks) >= 1
        assert task1 in high_priority_tasks
        assert task2 not in high_priority_tasks

    @pytest.mark.unit
    @pytest.mark.database
    def test_task_db_query_by_category(self, database_session):
        """Test querying TaskDB by category."""
        # Create tasks with different categories
        task1 = create_test_task_db(
            database_session,
            title="Frontend Task",
            category=TaskCategory.FRONTEND
        )
        task2 = create_test_task_db(
            database_session,
            title="Backend Task",
            category=TaskCategory.BACKEND
        )
        
        # Query by category
        frontend_tasks = database_session.query(TaskDB).filter(
            TaskDB.category == TaskCategory.FRONTEND
        ).all()
        
        assert len(frontend_tasks) >= 1
        assert task1 in frontend_tasks
        assert task2 not in frontend_tasks

    @pytest.mark.unit
    @pytest.mark.database
    def test_task_db_update(self, database_session):
        """Test updating TaskDB instance."""
        task_db = create_test_task_db(database_session, title="Original Title")
        original_updated_at = task_db.updated_at
        
        # Update the task
        task_db.title = "Updated Title"
        task_db.status = StatusEnum.EN_PROGRESO
        database_session.commit()
        database_session.refresh(task_db)
        
        assert task_db.title == "Updated Title"
        assert task_db.status == StatusEnum.EN_PROGRESO
        # updated_at should be automatically updated
        assert task_db.updated_at > original_updated_at

    @pytest.mark.unit
    @pytest.mark.database
    def test_task_db_delete(self, database_session):
        """Test deleting TaskDB instance."""
        task_db = create_test_task_db(database_session, title="To Delete")
        task_id = task_db.id
        
        # Delete the task
        database_session.delete(task_db)
        database_session.commit()
        
        # Verify it's deleted
        deleted_task = database_session.query(TaskDB).filter(TaskDB.id == task_id).first()
        assert deleted_task is None

    @pytest.mark.unit
    @pytest.mark.database
    def test_task_db_effort_validation(self, database_session):
        """Test TaskDB effort field validation."""
        task_db = TaskDB(title="Effort Test", effort=40)
        database_session.add(task_db)
        database_session.commit()
        database_session.refresh(task_db)
        
        assert task_db.effort == 40
        
        # Test negative effort (should be allowed by model)
        task_db.effort = -5
        database_session.commit()
        database_session.refresh(task_db)
        
        assert task_db.effort == -5

    @pytest.mark.unit
    @pytest.mark.database
    def test_task_db_costs_and_tokens(self, database_session):
        """Test TaskDB costs and tokens fields."""
        task_db = TaskDB(
            title="Cost Test",
            tokens_gastados=500,
            costos=2.50
        )
        database_session.add(task_db)
        database_session.commit()
        database_session.refresh(task_db)
        
        assert task_db.tokens_gastados == 500
        assert task_db.costos == 2.50 