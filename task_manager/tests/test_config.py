"""
Configuración específica para tests que evita problemas de inicialización del AIService.
"""
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

class TestConfig:
    """Configuración para tests."""
    TESTING = True
    DEBUG = False
    # Use SQLite for testing instead of Azure MySQL
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test-secret-key'
    # Disable Azure MySQL for tests
    AZURE_MYSQL_CONNECTION_STRING = None
    
    @property
    def TASKS_FILE(self):
        """Return a temporary file path for testing."""
        return Path(tempfile.gettempdir()) / 'test_tasks.json'

# Patchear las variables de entorno necesarias para testing
test_env_vars = {
    'AZURE_OPENAI_API_KEY': 'test_api_key',
    'AZURE_OPENAI_API_VERSION': '2023-12-01-preview',
    'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
    'AZURE_OPENAI_DEPLOYMENT_NAME': 'test-deployment',
    'TEMPERATURE': '0.5',
    'MAX_TOKENS': '500',
    'TOP_P': '0.2',
    'FREQUENCY_PENALTY': '0.0',
    'PRESENCE_PENALTY': '0.0'
}

# Aplicar las variables de entorno
for key, value in test_env_vars.items():
    os.environ[key] = value 