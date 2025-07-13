#!/usr/bin/env python3
"""
Script para subir el proyecto task_manager_final a GitHub
Este script automatiza la preparación y subida de archivos
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description, check=True):
    """Ejecuta un comando y maneja errores"""
    print(f"\n🔄 {description}...")
    print(f"Comando: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, check=check, capture_output=True, text=True, cwd='.')
        if result.stdout:
            print(f"✅ {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def get_repository_url():
    """Solicita la URL del repositorio GitHub"""
    print("\n📝 CONFIGURACIÓN DEL REPOSITORIO")
    print("=" * 50)
    
    while True:
        repo_url = input("🔗 Ingresa la URL de tu repositorio GitHub: ").strip()
        
        if not repo_url:
            print("❌ La URL no puede estar vacía")
            continue
            
        if not repo_url.startswith(('https://github.com/', 'git@github.com:')):
            print("❌ La URL debe ser de GitHub (https://github.com/... o git@github.com:...)")
            continue
            
        if not repo_url.endswith('.git'):
            repo_url += '.git'
            
        return repo_url

def get_commit_message():
    """Solicita el mensaje del commit"""
    default_message = "Initial commit: Task Manager with CI/CD pipeline"
    
    message = input(f"💬 Mensaje del commit (Enter para usar default): ").strip()
    
    return message if message else default_message

def initialize_git():
    """Inicializa el repositorio Git"""
    print("\n🔧 INICIALIZANDO REPOSITORIO GIT")
    print("=" * 40)
    
    # Verificar si ya es un repositorio Git
    if Path('.git').exists():
        print("📁 Repositorio Git ya existe")
        return True
    
    # Inicializar Git
    if not run_command(['git', 'init'], "Inicializando repositorio Git"):
        return False
    
    # Configurar usuario si no está configurado
    result = subprocess.run(['git', 'config', 'user.name'], capture_output=True, text=True)
    if not result.stdout.strip():
        name = input("👤 Ingresa tu nombre para Git: ").strip()
        if not run_command(['git', 'config', 'user.name', name], "Configurando nombre de usuario"):
            return False
    
    result = subprocess.run(['git', 'config', 'user.email'], capture_output=True, text=True)
    if not result.stdout.strip():
        email = input("📧 Ingresa tu email para Git: ").strip()
        if not run_command(['git', 'config', 'user.email', email], "Configurando email de usuario"):
            return False
    
    return True

def add_files():
    """Agrega archivos al repositorio"""
    print("\n📁 AGREGANDO ARCHIVOS AL REPOSITORIO")
    print("=" * 40)
    
    # Listar archivos que se van a agregar
    important_files = [
        '.github/workflows/ci-cd.yml',
        'task_manager/',
        'Dockerfile',
        'docker-compose.yml',
        'README.md',
        '.dockerignore',
        '.gitignore'
    ]
    
    print("📋 Archivos principales que se agregarán:")
    for file in important_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - NO ENCONTRADO")
    
    # Agregar todos los archivos
    if not run_command(['git', 'add', '.'], "Agregando todos los archivos"):
        return False
    
    # Mostrar estado
    run_command(['git', 'status', '--short'], "Mostrando estado del repositorio", check=False)
    
    return True

def commit_changes(message):
    """Hace commit de los cambios"""
    print(f"\n💾 HACIENDO COMMIT: {message}")
    print("=" * 50)
    
    return run_command(['git', 'commit', '-m', message], "Creando commit")

def add_remote(repo_url):
    """Agrega el remote origin"""
    print(f"\n🔗 CONFIGURANDO REMOTE: {repo_url}")
    print("=" * 50)
    
    # Verificar si ya existe el remote
    result = subprocess.run(['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"🔗 Remote origin ya existe: {result.stdout.strip()}")
        
        # Preguntar si cambiar
        change = input("¿Quieres cambiar la URL del remote? (y/N): ").strip().lower()
        if change == 'y':
            return run_command(['git', 'remote', 'set-url', 'origin', repo_url], "Actualizando remote origin")
        return True
    
    # Agregar nuevo remote
    return run_command(['git', 'remote', 'add', 'origin', repo_url], "Agregando remote origin")

def push_to_github():
    """Sube los cambios a GitHub"""
    print("\n🚀 SUBIENDO A GITHUB")
    print("=" * 30)
    
    # Configurar la rama principal
    run_command(['git', 'branch', '-M', 'main'], "Configurando rama principal", check=False)
    
    # Push inicial
    print("📤 Subiendo archivos a GitHub...")
    print("⚠️ Esto puede tomar unos minutos...")
    
    return run_command(['git', 'push', '-u', 'origin', 'main'], "Subiendo a GitHub")

def verify_upload():
    """Verifica que la subida fue exitosa"""
    print("\n✅ VERIFICACIÓN DE SUBIDA")
    print("=" * 30)
    
    # Mostrar información del repositorio
    run_command(['git', 'remote', '-v'], "Mostrando remotes configurados", check=False)
    run_command(['git', 'log', '--oneline', '-5'], "Mostrando últimos commits", check=False)
    
    print("\n🎉 SUBIDA COMPLETADA")
    print("=" * 25)
    print("✅ Archivos subidos a GitHub")
    print("✅ Pipeline CI/CD configurado")
    print("✅ Listo para activar el pipeline")
    
    # Obtener URL del repositorio web
    result = subprocess.run(['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True)
    if result.returncode == 0:
        repo_url = result.stdout.strip()
        if repo_url.endswith('.git'):
            repo_url = repo_url[:-4]
        
        print(f"\n🌐 Tu repositorio: {repo_url}")
        print(f"📊 GitHub Actions: {repo_url}/actions")
        print(f"⚙️ Settings: {repo_url}/settings")

def main():
    """Función principal"""
    print("🚀 SUBIR TASK MANAGER A GITHUB")
    print("=" * 40)
    print("Este script subirá tu proyecto a GitHub y activará el pipeline CI/CD")
    
    try:
        # Verificar que estamos en el directorio correcto
        if not Path('task_manager').exists() or not Path('.github').exists():
            print("❌ Error: No se encontraron los archivos del proyecto")
            print("Asegúrate de ejecutar este script desde el directorio del proyecto")
            return False
        
        # Obtener información del usuario
        repo_url = get_repository_url()
        commit_message = get_commit_message()
        
        # Confirmar antes de proceder
        print(f"\n📋 RESUMEN:")
        print(f"  • Repositorio: {repo_url}")
        print(f"  • Commit: {commit_message}")
        
        confirm = input("\n¿Continuar con la subida? (Y/n): ").strip().lower()
        if confirm == 'n':
            print("❌ Operación cancelada")
            return False
        
        # Ejecutar pasos
        if not initialize_git():
            return False
            
        if not add_files():
            return False
            
        if not commit_changes(commit_message):
            return False
            
        if not add_remote(repo_url):
            return False
            
        if not push_to_github():
            return False
            
        verify_upload()
        
        print("\n🎯 PRÓXIMOS PASOS:")
        print("1. Ir a tu repositorio en GitHub")
        print("2. Verificar que los archivos están subidos")
        print("3. Ir a la pestaña 'Actions' para ver el pipeline")
        print("4. El pipeline se ejecutará automáticamente")
        
        return True
        
    except KeyboardInterrupt:
        print("\n❌ Operación cancelada por el usuario")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPresiona Enter para salir...")
    sys.exit(0 if success else 1) 