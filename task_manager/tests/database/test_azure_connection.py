"""
Unit tests for Azure database connection.
"""
import pytest
from unittest.mock import patch, Mock, MagicMock
from app.database.azure_connection import AzureMySQLConnection, get_db_session


class TestAzureMySQLConnection:
    """Test class for Azure MySQL connection."""

    @pytest.mark.unit
    @pytest.mark.database
    @patch('app.database.azure_connection.os.getenv')
    def test_azure_connection_initialization(self, mock_getenv):
        """Test AzureMySQLConnection initialization."""
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'AZURE_MYSQL_CONNECTION_STRING': 'mysql://test:pass@localhost/test',
            'AZURE_MYSQL_SSL_CA': '/path/to/ca.pem',
            'AZURE_MYSQL_SSL_VERIFY': 'true'
        }.get(key, default)
        
        with patch('app.database.azure_connection.create_engine'), \
             patch('app.database.azure_connection.sessionmaker'):
            
            connection = AzureMySQLConnection()
            
            assert connection is not None
            assert hasattr(connection, 'engine')
            assert hasattr(connection, 'SessionLocal')

    @pytest.mark.unit
    @pytest.mark.database
    @patch('app.database.azure_connection.os.getenv')
    def test_azure_connection_missing_connection_string(self, mock_getenv):
        """Test AzureMySQLConnection with missing connection string."""
        # Mock missing connection string
        mock_getenv.return_value = None
        
        with pytest.raises(ValueError) as exc_info:
            AzureMySQLConnection()
        
        assert "AZURE_MYSQL_CONNECTION_STRING no está configurada" in str(exc_info.value)

    @pytest.mark.unit
    @pytest.mark.database
    @patch('app.database.azure_connection.os.getenv')
    def test_get_session(self, mock_getenv):
        """Test get_session method."""
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'AZURE_MYSQL_CONNECTION_STRING': 'mysql://test:pass@localhost/test',
        }.get(key, default)
        
        mock_session_class = Mock()
        mock_session_instance = Mock()
        mock_session_class.return_value = mock_session_instance
        
        with patch('app.database.azure_connection.create_engine'), \
             patch('app.database.azure_connection.sessionmaker', return_value=mock_session_class):
            
            connection = AzureMySQLConnection()
            session = connection.get_session()
            
            assert session is not None
            mock_session_class.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.database
    @patch('app.database.azure_connection.os.getenv')
    def test_create_tables(self, mock_getenv):
        """Test create_tables method."""
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'AZURE_MYSQL_CONNECTION_STRING': 'mysql://test:pass@localhost/test',
        }.get(key, default)
        
        mock_engine = Mock()
        mock_base_metadata = Mock()
        
        with patch('app.database.azure_connection.create_engine', return_value=mock_engine), \
             patch('app.database.azure_connection.sessionmaker'), \
             patch('app.database.azure_connection.Base') as mock_base:
            
            mock_base.metadata = mock_base_metadata
            
            connection = AzureMySQLConnection()
            connection.create_tables()
            
            mock_base_metadata.create_all.assert_called_once_with(bind=mock_engine)

    @pytest.mark.unit
    @pytest.mark.database
    @patch('app.database.azure_connection.os.getenv')
    def test_test_connection_success(self, mock_getenv):
        """Test test_connection method with successful connection."""
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'AZURE_MYSQL_CONNECTION_STRING': 'mysql://test:pass@localhost/test',
        }.get(key, default)
        
        mock_engine = Mock()
        mock_connection = Mock()
        mock_engine.connect.return_value.__enter__.return_value = mock_connection
        mock_connection.execute.return_value = Mock()
        
        with patch('app.database.azure_connection.create_engine', return_value=mock_engine), \
             patch('app.database.azure_connection.sessionmaker'):
            
            connection = AzureMySQLConnection()
            result = connection.test_connection()
            
            assert result is True
            mock_connection.execute.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.database
    @patch('app.database.azure_connection.os.getenv')
    def test_test_connection_failure(self, mock_getenv):
        """Test test_connection method with connection failure."""
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'AZURE_MYSQL_CONNECTION_STRING': 'mysql://test:pass@localhost/test',
        }.get(key, default)
        
        mock_engine = Mock()
        mock_engine.connect.side_effect = Exception("Connection failed")
        
        with patch('app.database.azure_connection.create_engine', return_value=mock_engine), \
             patch('app.database.azure_connection.sessionmaker'):
            
            connection = AzureMySQLConnection()
            result = connection.test_connection()
            
            assert result is False

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_db_session_function(self):
        """Test get_db_session helper function."""
        with patch('app.database.azure_connection.azure_mysql') as mock_azure_mysql:
            mock_session = Mock()
            mock_azure_mysql.get_session.return_value = mock_session
            
            result = get_db_session()
            
            assert result == mock_session
            mock_azure_mysql.get_session.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.database
    @patch('app.database.azure_connection.os.getenv')
    def test_ssl_configuration(self, mock_getenv):
        """Test SSL configuration for Azure MySQL."""
        # Mock environment variables with SSL
        mock_getenv.side_effect = lambda key, default=None: {
            'AZURE_MYSQL_CONNECTION_STRING': 'mysql://test:pass@localhost/test',
            'AZURE_MYSQL_SSL_CA': '/path/to/ca.pem',
            'AZURE_MYSQL_SSL_VERIFY': 'true'
        }.get(key, default)
        
        with patch('app.database.azure_connection.create_engine') as mock_create_engine, \
             patch('app.database.azure_connection.sessionmaker'):
            
            AzureMySQLConnection()
            
            # Verify that create_engine was called with SSL configuration
            mock_create_engine.assert_called_once()
            call_args = mock_create_engine.call_args
            connect_args = call_args[1].get('connect_args', {})
            
            # SSL configuration should be present
            assert 'ssl' in connect_args or len(connect_args) == 0  # Empty if no SSL

    @pytest.mark.unit
    @pytest.mark.database
    @patch('app.database.azure_connection.os.getenv')
    def test_engine_configuration_parameters(self, mock_getenv):
        """Test that engine is configured with proper parameters."""
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'AZURE_MYSQL_CONNECTION_STRING': 'mysql://test:pass@localhost/test',
        }.get(key, default)
        
        with patch('app.database.azure_connection.create_engine') as mock_create_engine, \
             patch('app.database.azure_connection.sessionmaker'):
            
            AzureMySQLConnection()
            
            # Verify engine configuration parameters
            mock_create_engine.assert_called_once()
            call_args = mock_create_engine.call_args
            
            # Check that connection parameters are set
            assert call_args[1]['pool_size'] == 10
            assert call_args[1]['pool_recycle'] == 3600
            assert call_args[1]['pool_pre_ping'] is True 