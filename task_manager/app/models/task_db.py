from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.azure_connection import Base
from app.models.enums import TaskCategory
import enum

class PriorityEnum(enum.Enum):
    """Enum para las prioridades de tareas"""
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    BLOQUEANTE = "bloqueante"

class StatusEnum(enum.Enum):
    """Enum para los estados de tareas"""
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    EN_REVISION = "en_revision"
    COMPLETADA = "completada"

class TaskDB(Base):
    """Modelo SQLAlchemy para la tabla Task en Azure MySQL"""
    
    __tablename__ = "tasks"
    
    # Campos principales
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Campos de prioridad y estado
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.MEDIA, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.PENDIENTE, nullable=False)
    
    # Campos de esfuerzo y asignación
    effort = Column(Integer, default=0, nullable=False)
    assigned_to = Column(String(100), nullable=True)
    assigned_role = Column(String(100), nullable=True)
    
    # Campos de categoría
    category = Column(Enum(TaskCategory), default=TaskCategory.OTRO, nullable=False)
    
    # Campos de análisis de riesgos
    risk_analysis = Column(Text, nullable=True)
    mitigation_plan = Column(Text, nullable=True)
    
    # Campos de tokens y costos
    tokens_gastados = Column(Integer, default=0, nullable=False)
    costos = Column(Float, default=0.0, nullable=False)
    
    # Campos de timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Campo de historia de usuario
    user_story_id = Column(Integer, ForeignKey('user_story.id'), nullable=True)
    user_story = relationship("UserStory", backref="tasks")
    
    def __repr__(self):
        return f"<TaskDB(id={self.id}, title='{self.title}', status='{self.status.value}')>"
    
    def to_dict(self):
        """Convierte el modelo a diccionario para compatibilidad con el modelo existente"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.value if self.priority else 'media',
            'effort': self.effort,
            'status': self.status.value if self.status else 'pendiente',
            'assigned_to': self.assigned_to,
            'assigned_role': self.assigned_role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'category': self.category.value if self.category else TaskCategory.OTRO.value,
            'risk_analysis': self.risk_analysis,
            'mitigation_plan': self.mitigation_plan,
            'tokens_gastados': self.tokens_gastados,
            'costos': self.costos,
            'user_story_id': self.user_story_id
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea una instancia del modelo desde un diccionario"""
        # Mapear valores de enum
        priority = PriorityEnum(data.get('priority', 'media'))
        status = StatusEnum(data.get('status', 'pendiente'))
        category = TaskCategory(data.get('category', TaskCategory.OTRO.value))
        
        return cls(
            id=data.get('id'),
            title=data.get('title', ''),
            description=data.get('description', ''),
            priority=priority,
            effort=data.get('effort', 0),
            status=status,
            assigned_to=data.get('assigned_to', ''),
            assigned_role=data.get('assigned_role', ''),
            category=category,
            risk_analysis=data.get('risk_analysis', ''),
            mitigation_plan=data.get('mitigation_plan', ''),
            tokens_gastados=data.get('tokens_gastados', 0),
            costos=data.get('costos', 0.0)
        ) 