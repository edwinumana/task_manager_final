#!/usr/bin/env python3
"""
Script de preparación del repositorio task_manager_final
Este script prepara la estructura correcta para el repositorio de GitHub
"""

import os
import shutil
import json
from pathlib import Path

def create_directory_structure():
    """Crea la estructura de directorios necesaria"""
    print("📁 Creando estructura de directorios...")
    
    # Directorios necesarios
    directories = [
        ".github/workflows",
        "task_manager/app",
        "task_manager/tests",
        "task_manager/data"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {directory}")

def verify_required_files():
    """Verifica que todos los archivos necesarios estén presentes"""
    print("\n🔍 Verificando archivos requeridos...")
    
    required_files = [
        ".github/workflows/ci-cd.yml",
        "task_manager/requirements.txt",
        "task_manager/run.py",
        "task_manager/config.py",
        "Dockerfile",
        "docker-compose.yml",
        "README.md",
        ".dockerignore"
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - FALTANTE")
            missing_files.append(file_path)
    
    return missing_files

def create_gitignore():
    """Crea un archivo .gitignore optimizado"""
    print("\n📝 Creando .gitignore...")
    
    gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Local development
.local/
local/
temp/
"""
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print("  ✅ .gitignore creado")

def update_docker_compose():
    """Actualiza el docker-compose.yml con la configuración correcta"""
    print("\n🐳 Actualizando docker-compose.yml...")
    
    # Leer el archivo actual si existe
    compose_content = """services:
  task-manager:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key-here
      # Configurar estas variables según tu configuración de Azure MySQL
      # - AZURE_MYSQL_CONNECTION_STRING=your-connection-string
      # - AZURE_MYSQL_SSL_CA=path-to-ca-cert
      # - AZURE_MYSQL_SSL_VERIFY=true
    volumes:
      # Montar directorio de datos para persistencia
      - ./task_manager/data:/app/data
    restart: unless-stopped
"""
    
    with open('docker-compose.yml', 'w', encoding='utf-8') as f:
        f.write(compose_content)
    
    print("  ✅ docker-compose.yml actualizado")

def create_repository_info():
    """Crea un archivo con información del repositorio"""
    print("\n📋 Creando información del repositorio...")
    
    repo_info = {
        "name": "task_manager_final",
        "description": "Task Manager - Sistema de Gestión de Tareas con CI/CD",
        "version": "1.0.0",
        "author": "Edwin Umaña Peña",
        "technologies": [
            "Python",
            "Flask",
            "Docker",
            "GitHub Actions",
            "Azure OpenAI",
            "Bootstrap"
        ],
        "features": [
            "CI/CD Pipeline automatizado",
            "Tests automatizados con pytest",
            "Containerización con Docker",
            "Integración con Azure OpenAI",
            "Interfaz web responsiva",
            "API REST completa"
        ],
        "deployment": {
            "docker_hub": "edwinumana/task-manager",
            "port": 5000,
            "health_check": "/tasks"
        }
    }
    
    with open('repository_info.json', 'w', encoding='utf-8') as f:
        json.dump(repo_info, f, indent=2, ensure_ascii=False)
    
    print("  ✅ repository_info.json creado")

def cleanup_unnecessary_files():
    """Limpia archivos innecesarios para el repositorio final"""
    print("\n🧹 Limpiando archivos innecesarios...")
    
    # Archivos y directorios a eliminar
    cleanup_items = [
        ".pytest_cache",
        ".venv",
        "scripts",
        "DEPLOYMENT_GUIDE.md",
        "DOCKER_README.md",
        "prepare_repository.py"  # Este mismo script
    ]
    
    for item in cleanup_items:
        item_path = Path(item)
        if item_path.exists():
            if item_path.is_file():
                item_path.unlink()
                print(f"  🗑️ Eliminado archivo: {item}")
            elif item_path.is_dir():
                shutil.rmtree(item_path)
                print(f"  🗑️ Eliminado directorio: {item}")

def generate_final_summary():
    """Genera un resumen final del repositorio"""
    print("\n📊 Generando resumen final...")
    
    # Contar archivos
    total_files = sum(1 for _ in Path('.').rglob('*') if _.is_file())
    
    # Verificar estructura
    structure_ok = all([
        Path('.github/workflows/ci-cd.yml').exists(),
        Path('task_manager/requirements.txt').exists(),
        Path('Dockerfile').exists(),
        Path('README.md').exists()
    ])
    
    summary = f"""
🎉 REPOSITORIO TASK_MANAGER_FINAL PREPARADO
==========================================

📊 Estadísticas:
  • Total de archivos: {total_files}
  • Estructura correcta: {'✅ SÍ' if structure_ok else '❌ NO'}

📁 Estructura principal:
  • .github/workflows/ci-cd.yml (Pipeline CI/CD)
  • task_manager/ (Código de la aplicación)
  • Dockerfile (Imagen Docker)
  • README.md (Documentación)
  • .dockerignore (Optimización)

🚀 Próximos pasos:
  1. Crear repositorio 'task_manager_final' en GitHub
  2. Configurar secretos DOCKER_USERNAME y DOCKER_PASSWORD
  3. Hacer git push para activar el pipeline
  4. Verificar despliegue en Docker Hub

📞 Soporte:
  • Revisar DEPLOYMENT_INSTRUCTIONS.md para pasos detallados
  • Consultar README.md para documentación completa
"""
    
    print(summary)
    
    # Guardar resumen en archivo
    with open('REPOSITORY_SUMMARY.md', 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print("  ✅ REPOSITORY_SUMMARY.md creado")

def main():
    """Función principal"""
    print("🚀 PREPARANDO REPOSITORIO TASK_MANAGER_FINAL")
    print("=" * 50)
    
    try:
        # Ejecutar pasos de preparación
        create_directory_structure()
        missing_files = verify_required_files()
        
        if missing_files:
            print(f"\n❌ Faltan {len(missing_files)} archivos críticos:")
            for file in missing_files:
                print(f"  • {file}")
            print("\n⚠️ Por favor, asegúrate de que todos los archivos estén presentes antes de continuar.")
            return False
        
        create_gitignore()
        update_docker_compose()
        create_repository_info()
        generate_final_summary()
        
        print("\n✅ REPOSITORIO PREPARADO EXITOSAMENTE")
        print("📦 Listo para subir a GitHub como 'task_manager_final'")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante la preparación: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 