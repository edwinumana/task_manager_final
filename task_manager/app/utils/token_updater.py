import json
from pathlib import Path
from typing import Dict, List
from app.models.task import Task

def update_tasks_with_tokens(tasks_file: Path) -> None:
    """
    Actualiza el archivo de tareas agregando los campos tokens_gastados y costos.
    Si una tarea ya tiene estos campos, mantiene sus valores.
    
    Args:
        tasks_file: Ruta al archivo JSON de tareas
    """
    try:
        # Leer el archivo JSON actual
        with open(tasks_file, 'r', encoding='utf-8') as f:
            tasks_data = json.load(f)
        
        # Convertir cada tarea a objeto Task y actualizar
        updated_tasks = []
        for task_data in tasks_data:
            # Si la tarea ya tiene los campos, mantener sus valores
            if 'tokens_gastados' not in task_data:
                task_data['tokens_gastados'] = 0
            if 'costos' not in task_data:
                task_data['costos'] = 0.0
            
            # Convertir a objeto Task y luego a diccionario para mantener el formato
            task = Task.from_dict(task_data)
            updated_tasks.append(task.to_dict())
        
        # Guardar el archivo actualizado
        with open(tasks_file, 'w', encoding='utf-8') as f:
            json.dump(updated_tasks, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        raise Exception(f"Error al actualizar el archivo de tareas: {str(e)}")

if __name__ == "__main__":
    # Ejecutar la actualización si se llama directamente
    base_dir = Path(__file__).resolve().parent.parent.parent
    tasks_file = base_dir / 'data' / 'tasks.json'
    update_tasks_with_tokens(tasks_file) 