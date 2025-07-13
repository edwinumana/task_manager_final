from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from app.models.enums import TaskCategory

class TaskSchema(BaseModel):
    """Schema Pydantic para validación de entrada de tareas"""
    
    title: str = Field(..., min_length=1, max_length=255, description="Título de la tarea")
    description: Optional[str] = Field(None, description="Descripción detallada de la tarea")
    priority: str = Field("media", description="Prioridad de la tarea")
    effort: int = Field(0, ge=0, le=1000, description="Esfuerzo estimado en horas")
    status: str = Field("pendiente", description="Estado actual de la tarea")
    assigned_to: Optional[str] = Field(None, max_length=100, description="Persona asignada")
    assigned_role: Optional[str] = Field(None, max_length=100, description="Rol de la persona asignada")
    category: str = Field(TaskCategory.OTRO.value, description="Categoría de la tarea")
    risk_analysis: Optional[str] = Field(None, description="Análisis de riesgos")
    mitigation_plan: Optional[str] = Field(None, description="Plan de mitigación")
    tokens_gastados: int = Field(0, ge=0, description="Tokens gastados en IA")
    costos: float = Field(0.0, ge=0.0, description="Costos en dólares")
    
    @validator('priority')
    def validate_priority(cls, v):
        valid_priorities = ['baja', 'media', 'alta', 'bloqueante']
        if v not in valid_priorities:
            raise ValueError(f'Prioridad debe ser una de: {", ".join(valid_priorities)}')
        return v
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ['pendiente', 'en_progreso', 'en_revision', 'completada']
        if v not in valid_statuses:
            raise ValueError(f'Estado debe ser uno de: {", ".join(valid_statuses)}')
        return v
    
    @validator('category')
    def validate_category(cls, v):
        valid_categories = TaskCategory.get_values()
        if v not in valid_categories:
            raise ValueError(f'Categoría debe ser una de: {", ".join(valid_categories)}')
        return v
    
    @validator('effort')
    def validate_effort(cls, v):
        if v < 0:
            raise ValueError('El esfuerzo no puede ser negativo')
        if v > 1000:
            raise ValueError('El esfuerzo no puede exceder 1000 horas')
        return v
    
    @validator('tokens_gastados')
    def validate_tokens(cls, v):
        if v < 0:
            raise ValueError('Los tokens gastados no pueden ser negativos')
        return v
    
    @validator('costos')
    def validate_costos(cls, v):
        if v < 0:
            raise ValueError('Los costos no pueden ser negativos')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Análisis de control de calidad",
                "description": "Realizar análisis de control de calidad para el lote 2024-001",
                "priority": "alta",
                "effort": 8,
                "status": "pendiente",
                "assigned_to": "Juan Pérez",
                "assigned_role": "Analista",
                "category": "testing",
                "risk_analysis": "Riesgos identificados en el proceso",
                "mitigation_plan": "Plan de mitigación para los riesgos",
                "tokens_gastados": 1500,
                "costos": 0.025
            }
        } 