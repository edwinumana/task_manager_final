"""
Unit tests for the AIService.
"""
import pytest
from unittest.mock import patch, Mock, MagicMock
from app.services.ai_service import AIService


class TestAIService:
    """Test class for AIService."""

    @pytest.mark.unit
    @pytest.mark.ai
    def test_ai_service_initialization(self, mock_azure_openai):
        """Test AIService initialization."""
        service = AIService()
        
        assert service is not None
        assert hasattr(service, 'client')
        assert hasattr(service, 'deployment_name')
        assert hasattr(service, 'temperature')
        assert hasattr(service, 'max_tokens')

    @pytest.mark.unit
    @pytest.mark.ai
    def test_ai_service_initialization_missing_credentials(self):
        """Test AIService initialization with missing credentials."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(Exception) as exc_info:
                AIService()
            assert "Faltan credenciales" in str(exc_info.value)

    @pytest.mark.unit
    @pytest.mark.ai
    def test_count_tokens(self, mock_azure_openai):
        """Test count_tokens method."""
        service = AIService()
        
        # Test with simple text
        token_count = service.count_tokens("Hello world")
        assert isinstance(token_count, int)
        assert token_count > 0
        
        # Test with empty text
        token_count_empty = service.count_tokens("")
        assert token_count_empty == 0

    @pytest.mark.unit
    @pytest.mark.ai
    def test_calculate_cost(self, mock_azure_openai):
        """Test calculate_cost method."""
        service = AIService()
        
        # Test cost calculation
        cost = service.calculate_cost(100, 50)
        expected_cost = (100 / 1000) * 0.01 + (50 / 1000) * 0.03
        assert cost == expected_cost
        
        # Test with zero tokens
        cost_zero = service.calculate_cost(0, 0)
        assert cost_zero == 0.0

    @pytest.mark.unit
    @pytest.mark.ai
    def test_call_llm_success(self, mock_azure_openai):
        """Test _call_llm method with successful response."""
        service = AIService()
        
        # Mock the response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test AI response"
        mock_azure_openai.chat.completions.create.return_value = mock_response
        
        # Call the method
        response, token_info = service._call_llm(
            "Test system prompt",
            "Test user prompt"
        )
        
        # Assertions
        assert response == "Test AI response"
        assert isinstance(token_info, dict)
        assert 'input_tokens' in token_info
        assert 'output_tokens' in token_info
        assert 'total_tokens' in token_info
        assert 'cost' in token_info

    @pytest.mark.unit
    @pytest.mark.ai
    def test_call_llm_rate_limit_error(self, mock_azure_openai):
        """Test _call_llm method with rate limit error."""
        service = AIService()
        
        # Mock rate limit error
        mock_azure_openai.chat.completions.create.side_effect = Exception("429 Too Many Requests")
        
        # Call the method and expect exception
        with pytest.raises(Exception) as exc_info:
            service._call_llm("Test system prompt", "Test user prompt")
        
        assert "límite de solicitudes" in str(exc_info.value)

    @pytest.mark.unit
    @pytest.mark.ai
    def test_call_llm_authentication_error(self, mock_azure_openai):
        """Test _call_llm method with authentication error."""
        service = AIService()
        
        # Mock authentication error
        mock_azure_openai.chat.completions.create.side_effect = Exception("authentication failed")
        
        # Call the method and expect exception
        with pytest.raises(Exception) as exc_info:
            service._call_llm("Test system prompt", "Test user prompt")
        
        assert "autenticación" in str(exc_info.value)

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_description(self, mock_ai_service):
        """Test generate_description method."""
        result = mock_ai_service.generate_description("Test task title")
        
        assert isinstance(result, dict)
        assert 'description' in result
        assert 'tokens_gastados' in result
        assert 'costos' in result

    @pytest.mark.unit
    @pytest.mark.ai
    def test_categorize_task(self, mock_ai_service):
        """Test categorize_task method."""
        result = mock_ai_service.categorize_task(
            "Test task title",
            "Test description"
        )
        
        assert isinstance(result, dict)
        assert 'category' in result
        assert 'tokens_gastados' in result
        assert 'costos' in result

    @pytest.mark.unit
    @pytest.mark.ai
    def test_estimate_effort(self, mock_ai_service):
        """Test estimate_effort method."""
        result = mock_ai_service.estimate_effort(
            "Test task title",
            "Test description",
            "desarrollo"
        )
        
        assert isinstance(result, dict)
        assert 'effort' in result
        assert 'tokens_gastados' in result
        assert 'costos' in result

    @pytest.mark.unit
    @pytest.mark.ai
    def test_analyze_risks(self, mock_ai_service):
        """Test analyze_risks method."""
        result = mock_ai_service.analyze_risks(
            "Test task title",
            "Test description",
            "desarrollo"
        )
        
        assert isinstance(result, dict)
        assert 'risk_analysis' in result
        assert 'tokens_gastados' in result
        assert 'costos' in result

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_mitigation(self, mock_ai_service):
        """Test generate_mitigation method."""
        result = mock_ai_service.generate_mitigation(
            "Test task title",
            "Test description",
            "desarrollo",
            "Test risk analysis"
        )
        
        assert isinstance(result, dict)
        assert 'mitigation_plan' in result
        assert 'tokens_gastados' in result
        assert 'costos' in result

    @pytest.mark.unit
    @pytest.mark.ai
    @patch('app.services.ai_service.AIService._call_llm')
    def test_process_task(self, mock_call_llm, mock_azure_openai):
        """Test process_task method."""
        # Setup mock responses for each AI call
        mock_call_llm.side_effect = [
            ("Generated description", {"total_tokens": 50, "cost": 0.005}),
            ("desarrollo", {"total_tokens": 30, "cost": 0.003}),
            ("8", {"total_tokens": 40, "cost": 0.004}),
            ("Risk analysis", {"total_tokens": 60, "cost": 0.006}),
            ("Mitigation plan", {"total_tokens": 70, "cost": 0.007})
        ]
        
        service = AIService()
        task_data = {
            'title': 'Test Task',
            'description': 'Original description'
        }
        
        result = service.process_task(task_data)
        
        # Assertions
        assert isinstance(result, dict)
        assert result['description'] == "Generated description"
        assert result['category'] == "desarrollo"
        assert result['effort'] == 8
        assert result['risk_analysis'] == "Risk analysis"
        assert result['risk_mitigation'] == "Mitigation plan"
        assert result['tokens_gastados'] == 250  # Sum of all tokens
        assert result['costos'] == 0.025  # Sum of all costs

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_user_story_method_exists(self, mock_azure_openai):
        """Test that generate_user_story method exists."""
        service = AIService()
        assert hasattr(service, 'generate_user_story')

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_tasks_method_exists(self, mock_azure_openai):
        """Test that generate_tasks method exists."""
        service = AIService()
        assert hasattr(service, 'generate_tasks')

    @pytest.mark.unit
    @pytest.mark.ai
    @patch('app.services.ai_service.AIService._call_llm')
    def test_process_task_invalid_effort(self, mock_call_llm, mock_azure_openai):
        """Test process_task method with invalid effort response."""
        # Setup mock responses with invalid effort
        mock_call_llm.side_effect = [
            ("Generated description", {"total_tokens": 50, "cost": 0.005}),
            ("desarrollo", {"total_tokens": 30, "cost": 0.003}),
            ("invalid_number", {"total_tokens": 40, "cost": 0.004}),
            ("Risk analysis", {"total_tokens": 60, "cost": 0.006}),
            ("Mitigation plan", {"total_tokens": 70, "cost": 0.007})
        ]
        
        service = AIService()
        task_data = {
            'title': 'Test Task',
            'description': 'Original description'
        }
        
        result = service.process_task(task_data)
        
        # Should default to 0 for invalid effort
        assert result['effort'] == 0

    @pytest.mark.unit
    @pytest.mark.ai
    def test_ai_service_parameters_configuration(self, mock_azure_openai):
        """Test that AI service parameters are properly configured."""
        service = AIService()
        
        # Check default parameter values
        assert service.temperature == 0.5
        assert service.max_tokens == 500
        assert service.top_p == 0.2
        assert service.frequency_penalty == 0.0
        assert service.presence_penalty == 0.0

    @pytest.mark.unit
    @pytest.mark.ai
    def test_ai_service_encoding_initialization(self, mock_azure_openai):
        """Test that encoding is properly initialized."""
        service = AIService()
        
        assert hasattr(service, 'encoding')
        assert service.encoding is not None 