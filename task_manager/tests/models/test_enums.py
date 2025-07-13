"""
Unit tests for the enums module.
"""
import pytest
from app.models.enums import TaskCategory
from app.models.task_db import StatusEnum, PriorityEnum


class TestTaskCategory:
    """Test class for TaskCategory enum."""

    @pytest.mark.unit
    def test_task_category_values(self):
        """Test TaskCategory enum values."""
        assert TaskCategory.TESTING.value == "testing"
        assert TaskCategory.FRONTEND.value == "frontend"
        assert TaskCategory.BACKEND.value == "backend"
        assert TaskCategory.DESARROLLO.value == "desarrollo"
        assert TaskCategory.DISEÑO.value == "diseño"
        assert TaskCategory.DOCUMENTACION.value == "documentacion"
        assert TaskCategory.BASE_DE_DATOS.value == "base_de_datos"
        assert TaskCategory.SEGURIDAD.value == "seguridad"
        assert TaskCategory.INFRAESTRUCTURA.value == "infraestructura"
        assert TaskCategory.MANTENIMIENTO.value == "mantenimiento"
        assert TaskCategory.INVESTIGACION.value == "investigacion"
        assert TaskCategory.SUPERVISION.value == "supervision"
        assert TaskCategory.RIESGOS_LABORALES.value == "riesgos_laborales"
        assert TaskCategory.LIMPIEZA.value == "limpieza"
        assert TaskCategory.OTRO.value == "otro"

    @pytest.mark.unit
    def test_task_category_get_values(self):
        """Test TaskCategory get_values class method."""
        values = TaskCategory.get_values()
        
        assert isinstance(values, list)
        assert len(values) == 15  # Total number of categories
        assert "testing" in values
        assert "frontend" in values
        assert "backend" in values
        assert "desarrollo" in values
        assert "otro" in values

    @pytest.mark.unit
    def test_task_category_get_display_names(self):
        """Test TaskCategory get_display_names method if it exists."""
        if hasattr(TaskCategory, 'get_display_names'):
            display_names = TaskCategory.get_display_names()
            assert isinstance(display_names, dict)
            assert len(display_names) > 0

    @pytest.mark.unit
    def test_task_category_enum_iteration(self):
        """Test iterating over TaskCategory enum."""
        categories = list(TaskCategory)
        
        assert len(categories) == 15
        assert TaskCategory.TESTING in categories
        assert TaskCategory.OTRO in categories

    @pytest.mark.unit
    def test_task_category_membership(self):
        """Test TaskCategory membership."""
        assert TaskCategory.TESTING in TaskCategory
        assert TaskCategory.FRONTEND in TaskCategory
        assert TaskCategory.OTRO in TaskCategory


class TestStatusEnum:
    """Test class for StatusEnum."""

    @pytest.mark.unit
    def test_status_enum_values(self):
        """Test StatusEnum values."""
        assert StatusEnum.PENDIENTE.value == "pendiente"
        assert StatusEnum.EN_PROGRESO.value == "en_progreso"
        assert StatusEnum.EN_REVISION.value == "en_revision"
        assert StatusEnum.COMPLETADA.value == "completada"

    @pytest.mark.unit
    def test_status_enum_count(self):
        """Test StatusEnum has correct number of values."""
        statuses = list(StatusEnum)
        assert len(statuses) == 4

    @pytest.mark.unit
    def test_status_enum_iteration(self):
        """Test iterating over StatusEnum."""
        statuses = list(StatusEnum)
        
        assert StatusEnum.PENDIENTE in statuses
        assert StatusEnum.EN_PROGRESO in statuses
        assert StatusEnum.EN_REVISION in statuses
        assert StatusEnum.COMPLETADA in statuses


class TestPriorityEnum:
    """Test class for PriorityEnum."""

    @pytest.mark.unit
    def test_priority_enum_values(self):
        """Test PriorityEnum values."""
        assert PriorityEnum.BAJA.value == "baja"
        assert PriorityEnum.MEDIA.value == "media"
        assert PriorityEnum.ALTA.value == "alta"
        assert PriorityEnum.BLOQUEANTE.value == "bloqueante"

    @pytest.mark.unit
    def test_priority_enum_count(self):
        """Test PriorityEnum has correct number of values."""
        priorities = list(PriorityEnum)
        assert len(priorities) == 4

    @pytest.mark.unit
    def test_priority_enum_iteration(self):
        """Test iterating over PriorityEnum."""
        priorities = list(PriorityEnum)
        
        assert PriorityEnum.BAJA in priorities
        assert PriorityEnum.MEDIA in priorities
        assert PriorityEnum.ALTA in priorities
        assert PriorityEnum.BLOQUEANTE in priorities

    @pytest.mark.unit
    def test_priority_enum_membership(self):
        """Test PriorityEnum membership."""
        assert PriorityEnum.BAJA in PriorityEnum
        assert PriorityEnum.MEDIA in PriorityEnum
        assert PriorityEnum.ALTA in PriorityEnum
        assert PriorityEnum.BLOQUEANTE in PriorityEnum 