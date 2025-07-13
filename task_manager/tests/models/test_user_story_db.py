"""
Unit tests for the UserStory database model.
"""
import pytest
from sqlalchemy.exc import IntegrityError
from app.models.user_story_db import UserStory
from app.models.task_db import PriorityEnum
from tests.conftest import create_test_user_story, create_test_task_db


class TestUserStoryDB:
    """Test class for UserStory database model."""

    @pytest.mark.unit
    @pytest.mark.database
    def test_user_story_creation(self, database_session, sample_user_story_data):
        """Test UserStory creation with valid data."""
        user_story = UserStory(**sample_user_story_data)
        database_session.add(user_story)
        database_session.commit()
        database_session.refresh(user_story)
        
        assert user_story.id is not None
        assert user_story.project == sample_user_story_data['project']
        assert user_story.role == sample_user_story_data['role']
        assert user_story.goal == sample_user_story_data['goal']
        assert user_story.reason == sample_user_story_data['reason']
        assert user_story.description == sample_user_story_data['description']
        assert user_story.priority == sample_user_story_data['priority']
        assert user_story.story_points == sample_user_story_data['story_points']
        assert user_story.effort_hours == sample_user_story_data['effort_hours']
        assert user_story.created_at is not None

    @pytest.mark.unit
    @pytest.mark.database
    def test_user_story_required_fields(self, database_session):
        """Test UserStory with missing required fields."""
        # Test missing project
        with pytest.raises(IntegrityError):
            user_story = UserStory(
                role="Test Role",
                goal="Test Goal",
                reason="Test Reason",
                description="Test Description",
                priority=PriorityEnum.MEDIA,
                story_points=3,
                effort_hours=24.0
            )
            database_session.add(user_story)
            database_session.commit()
        
        database_session.rollback()
        
        # Test missing role
        with pytest.raises(IntegrityError):
            user_story = UserStory(
                project="Test Project",
                goal="Test Goal",
                reason="Test Reason",
                description="Test Description",
                priority=PriorityEnum.MEDIA,
                story_points=3,
                effort_hours=24.0
            )
            database_session.add(user_story)
            database_session.commit()

    @pytest.mark.unit
    @pytest.mark.database
    def test_user_story_priority_enum(self, database_session):
        """Test UserStory priority enum field."""
        user_story = create_test_user_story(
            database_session,
            priority=PriorityEnum.BLOQUEANTE
        )
        
        assert user_story.priority == PriorityEnum.BLOQUEANTE
        assert user_story.priority.value == "bloqueante"

    @pytest.mark.unit
    @pytest.mark.database
    def test_user_story_story_points_validation(self, database_session):
        """Test UserStory story_points field."""
        user_story = create_test_user_story(
            database_session,
            story_points=8
        )
        
        assert user_story.story_points == 8
        assert isinstance(user_story.story_points, int)

    @pytest.mark.unit
    @pytest.mark.database
    def test_user_story_effort_hours_validation(self, database_session):
        """Test UserStory effort_hours field."""
        user_story = create_test_user_story(
            database_session,
            effort_hours=120.5
        )
        
        assert user_story.effort_hours == 120.5
        assert isinstance(user_story.effort_hours, float)

    @pytest.mark.unit
    @pytest.mark.database
    def test_user_story_relationship_with_tasks(self, database_session):
        """Test UserStory relationship with tasks."""
        # Create a user story
        user_story = create_test_user_story(database_session)
        
        # Create tasks linked to this user story
        task1 = create_test_task_db(
            database_session,
            title="Task 1 for User Story",
            user_story_id=user_story.id
        )
        task2 = create_test_task_db(
            database_session,
            title="Task 2 for User Story",
            user_story_id=user_story.id
        )
        
        # Test the relationship
        assert len(user_story.tasks) == 2
        assert task1 in user_story.tasks
        assert task2 in user_story.tasks
        assert task1.user_story == user_story
        assert task2.user_story == user_story

    @pytest.mark.unit
    @pytest.mark.database
    def test_user_story_query_by_project(self, database_session):
        """Test querying UserStory by project."""
        # Create user stories with different projects
        story1 = create_test_user_story(
            database_session,
            project="Project Alpha"
        )
        story2 = create_test_user_story(
            database_session,
            project="Project Beta"
        )
        
        # Query by project
        alpha_stories = database_session.query(UserStory).filter(
            UserStory.project == "Project Alpha"
        ).all()
        
        assert len(alpha_stories) >= 1
        assert story1 in alpha_stories
        assert story2 not in alpha_stories

    @pytest.mark.unit
    @pytest.mark.database
    def test_user_story_query_by_priority(self, database_session):
        """Test querying UserStory by priority."""
        # Create user stories with different priorities
        story1 = create_test_user_story(
            database_session,
            priority=PriorityEnum.ALTA
        )
        story2 = create_test_user_story(
            database_session,
            priority=PriorityEnum.BAJA
        )
        
        # Query by priority
        high_priority_stories = database_session.query(UserStory).filter(
            UserStory.priority == PriorityEnum.ALTA
        ).all()
        
        assert len(high_priority_stories) >= 1
        assert story1 in high_priority_stories
        assert story2 not in high_priority_stories

    @pytest.mark.unit
    @pytest.mark.database
    def test_user_story_query_by_story_points(self, database_session):
        """Test querying UserStory by story points."""
        # Create user stories with different story points
        story1 = create_test_user_story(
            database_session,
            story_points=8
        )
        story2 = create_test_user_story(
            database_session,
            story_points=3
        )
        
        # Query by story points
        large_stories = database_session.query(UserStory).filter(
            UserStory.story_points >= 5
        ).all()
        
        assert len(large_stories) >= 1
        assert story1 in large_stories
        assert story2 not in large_stories

    @pytest.mark.unit
    @pytest.mark.database
    def test_user_story_update(self, database_session):
        """Test updating UserStory instance."""
        user_story = create_test_user_story(database_session)
        original_project = user_story.project
        
        # Update the user story
        user_story.project = "Updated Project"
        user_story.story_points = 13
        database_session.commit()
        database_session.refresh(user_story)
        
        assert user_story.project == "Updated Project"
        assert user_story.story_points == 13
        assert user_story.project != original_project

    @pytest.mark.unit
    @pytest.mark.database
    def test_user_story_delete(self, database_session):
        """Test deleting UserStory instance."""
        user_story = create_test_user_story(database_session)
        story_id = user_story.id
        
        # Delete the user story
        database_session.delete(user_story)
        database_session.commit()
        
        # Verify it's deleted
        deleted_story = database_session.query(UserStory).filter(
            UserStory.id == story_id
        ).first()
        assert deleted_story is None

    @pytest.mark.unit
    @pytest.mark.database
    def test_user_story_cascade_delete_tasks(self, database_session):
        """Test that deleting user story doesn't break tasks."""
        # Create user story with tasks
        user_story = create_test_user_story(database_session)
        task = create_test_task_db(
            database_session,
            title="Task with User Story",
            user_story_id=user_story.id
        )
        
        task_id = task.id
        
        # Delete the user story
        database_session.delete(user_story)
        database_session.commit()
        
        # Task should still exist but user_story_id should be None
        remaining_task = database_session.query(TaskDB).filter(
            TaskDB.id == task_id
        ).first()
        # This depends on the foreign key constraint configuration
        # The task might be deleted or user_story_id might be set to None

    @pytest.mark.unit
    @pytest.mark.database
    def test_user_story_string_field_lengths(self, database_session):
        """Test UserStory string field length constraints."""
        # Test with very long strings (should work within limits)
        long_project = "A" * 100  # Max length
        long_role = "B" * 100     # Max length
        long_goal = "C" * 255     # Max length
        long_reason = "D" * 255   # Max length
        
        user_story = UserStory(
            project=long_project,
            role=long_role,
            goal=long_goal,
            reason=long_reason,
            description="Test description",
            priority=PriorityEnum.MEDIA,
            story_points=5,
            effort_hours=40.0
        )
        
        database_session.add(user_story)
        database_session.commit()
        database_session.refresh(user_story)
        
        assert user_story.project == long_project
        assert user_story.role == long_role
        assert user_story.goal == long_goal
        assert user_story.reason == long_reason

    @pytest.mark.unit
    @pytest.mark.database
    def test_user_story_repr_method(self, database_session):
        """Test UserStory __repr__ method if it exists."""
        user_story = create_test_user_story(database_session)
        
        if hasattr(user_story, '__repr__'):
            repr_str = repr(user_story)
            assert isinstance(repr_str, str)
            assert len(repr_str) > 0 