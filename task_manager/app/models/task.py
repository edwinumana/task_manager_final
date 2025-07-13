from datetime import datetime
from typing import Dict, Optional
from .enums import TaskCategory

class Task:
    """
    Modelo que representa una tarea en el sistema.
    Esta clase define la estructura de una tarea y proporciona métodos para
    convertir entre objetos Task y diccionarios (para almacenamiento JSON).
    """
    
    # Valores permitidos para prioridad y estado
    VALID_PRIORITIES = ['baja', 'media', 'alta', 'bloqueante']
    VALID_STATUSES = ['pendiente', 'en_progreso', 'en_revision', 'completada']
    
    def __init__(self, id: Optional[int] = None, title: str = '', description: str = '', 
                 priority: str = 'media', effort: int = 0, status: str = 'pendiente',
                 assigned_to: str = '', assigned_role: str = '', created_at: Optional[str] = None, 
                 updated_at: Optional[str] = None, category: str = TaskCategory.OTRO.value,
                 risk_analysis: str = '', mitigation_plan: str = '', tokens_gastados: int = 0,
                 costos: float = 0.0):
        """
        Inicializa una nueva tarea.
        
        Args:
            id: Identificador único de la tarea
            title: Título de la tarea
            description: Descripción detallada
            priority: Prioridad (debe ser uno de VALID_PRIORITIES)
            effort: Horas estimadas de trabajo
            status: Estado actual (debe ser uno de VALID_STATUSES)
            assigned_to: Persona del equipo asignada a la tarea
            assigned_role: Cargo de la persona asignada
            created_at: Fecha de creación (opcional)
            updated_at: Fecha de última actualización (opcional)
            category: Categoría de la tarea (debe ser uno de TaskCategory)
            risk_analysis: Análisis de riesgos de la tarea
            mitigation_plan: Plan de mitigación de riesgos
            tokens_gastados: Número total de tokens utilizados en la tarea
            costos: Costo total en dólares de los tokens utilizados
        """
        self.id = id
        self.title = title
        self.description = description
        # Valida y asigna la prioridad, si no es válida usa 'media' por defecto
        self.priority = priority if priority in self.VALID_PRIORITIES else 'media'
        # Manejar la conversión del campo effort
        try:
            self.effort = int(effort) if effort and str(effort).strip() else 0
        except (ValueError, TypeError):
            self.effort = 0
        # Valida y asigna el estado, si no es válido usa 'pendiente' por defecto
        self.status = status if status in self.VALID_STATUSES else 'pendiente'
        self.assigned_to = assigned_to
        self.assigned_role = assigned_role
        # Si no se proporciona fecha, usa la fecha actual
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()
        # Valida y asigna la categoría
        self.category = category if category in TaskCategory.get_values() else TaskCategory.OTRO.value
        self.risk_analysis = risk_analysis
        self.mitigation_plan = mitigation_plan
        self.tokens_gastados = tokens_gastados
        self.costos = costos
    
    def to_dict(self) -> Dict:
        """
        Convierte el objeto Task a un diccionario para almacenamiento JSON.
        
        Returns:
            Dict: Diccionario con los datos de la tarea
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'effort': self.effort,
            'status': self.status,
            'assigned_to': self.assigned_to,
            'assigned_role': self.assigned_role,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'category': self.category,
            'risk_analysis': self.risk_analysis,
            'mitigation_plan': self.mitigation_plan,
            'tokens_gastados': self.tokens_gastados,
            'costos': self.costos
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """
        Crea un objeto Task desde un diccionario.
        
        Args:
            data: Diccionario con los datos de la tarea
            
        Returns:
            Task: Nueva instancia de Task con los datos proporcionados
        """
        # Manejar la compatibilidad con el campo risk_mitigation antiguo
        mitigation_plan = data.get('mitigation_plan', '')
        if not mitigation_plan and 'risk_mitigation' in data:
            mitigation_plan = data['risk_mitigation']
        
        # Convertir tokens_gastados y costos a números
        tokens_gastados = data.get('tokens_gastados', 0)
        costos = data.get('costos', 0.0)
        
        try:
            tokens_gastados = int(tokens_gastados) if tokens_gastados else 0
        except (ValueError, TypeError):
            tokens_gastados = 0
            
        try:
            costos = float(costos) if costos else 0.0
        except (ValueError, TypeError):
            costos = 0.0
        
        return cls(
            id=data.get('id'),
            title=data.get('title', ''),
            description=data.get('description', ''),
            priority=data.get('priority', 'media'),
            effort=data.get('effort', 0),
            status=data.get('status', 'pendiente'),
            assigned_to=data.get('assigned_to', ''),
            assigned_role=data.get('assigned_role', ''),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            category=data.get('category', TaskCategory.OTRO.value),
            risk_analysis=data.get('risk_analysis', ''),
            mitigation_plan=mitigation_plan,
            tokens_gastados=tokens_gastados,
            costos=costos
        )
    
    def update(self, **kwargs):
        """
        Actualiza los campos de la tarea.
        Solo actualiza los campos válidos y mantiene las validaciones.
        
        Args:
            **kwargs: Campos a actualizar con sus nuevos valores
        """
        # Lista de campos que pueden ser actualizados
        updatable_fields = ['title', 'description', 'priority', 
                           'effort', 'status', 'assigned_to', 'assigned_role',
                           'category', 'risk_analysis', 'mitigation_plan',
                           'tokens_gastados', 'costos']
        
        for field, value in kwargs.items():
            if field in updatable_fields and hasattr(self, field):
                # Validaciones específicas para cada campo
                if field == 'priority' and value not in self.VALID_PRIORITIES:
                    continue
                if field == 'status' and value not in self.VALID_STATUSES:
                    continue
                if field == 'category' and value not in TaskCategory.get_values():
                    continue
                if field == 'effort':
                    value = int(value)
                setattr(self, field, value)
        
        # Actualiza la fecha de modificación
        self.updated_at = datetime.now().isoformat()
    
    def __repr__(self):
        """Representación en string del objeto Task"""
        return f"<Task {self.id}: {self.title}>"