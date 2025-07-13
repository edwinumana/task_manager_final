from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .task_schema import TaskSchema

class TaskResponseSchema(BaseModel):
    """Schema Pydantic para respuesta de una tarea individual"""
    
    id: int = Field(..., description="ID único de la tarea")
    title: str = Field(..., description="Título de la tarea")
    description: Optional[str] = Field(None, description="Descripción detallada de la tarea")
    priority: str = Field(..., description="Prioridad de la tarea")
    effort: int = Field(..., description="Esfuerzo estimado en horas")
    status: str = Field(..., description="Estado actual de la tarea")
    assigned_to: Optional[str] = Field(None, description="Persona asignada")
    assigned_role: Optional[str] = Field(None, description="Rol de la persona asignada")
    created_at: str = Field(..., description="Fecha de creación")
    updated_at: str = Field(..., description="Fecha de última actualización")
    category: str = Field(..., description="Categoría de la tarea")
    risk_analysis: Optional[str] = Field(None, description="Análisis de riesgos")
    mitigation_plan: Optional[str] = Field(None, description="Plan de mitigación")
    tokens_gastados: int = Field(..., description="Tokens gastados en IA")
    costos: float = Field(..., description="Costos en dólares")
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Análisis de control de calidad",
                "description": "Realizar análisis de control de calidad para el lote 2024-001",
                "priority": "alta",
                "effort": 8,
                "status": "pendiente",
                "assigned_to": "Juan Pérez",
                "assigned_role": "Analista",
                "category": "testing",
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00",
                "risk_analysis": "Riesgos identificados en el proceso",
                "mitigation_plan": "Plan de mitigación para los riesgos",
                "tokens_gastados": 1500,
                "costos": 0.025
            }
        }

class TaskSchemas(BaseModel):
    """Schema Pydantic para respuesta de múltiples tareas"""
    
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    tasks: List[TaskResponseSchema] = Field(..., description="Lista de tareas")
    total: int = Field(..., description="Total de tareas")
    total_tokens: int = Field(0, description="Total de tokens gastados")
    total_costos: float = Field(0.0, description="Total de costos en dólares")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "tasks": [
                    {
                        "id": 1,
                        "title": "Análisis de control de calidad",
                        "description": "Realizar análisis de control de calidad",
                        "priority": "alta",
                        "effort": 8,
                        "status": "pendiente",
                        "assigned_to": "Juan Pérez",
                        "assigned_role": "Analista",
                        "category": "testing",
                        "created_at": "2024-01-15T10:30:00",
                        "updated_at": "2024-01-15T10:30:00",
                        "risk_analysis": "Riesgos identificados",
                        "mitigation_plan": "Plan de mitigación",
                        "tokens_gastados": 1500,
                        "costos": 0.025
                    }
                ],
                "total": 1,
                "total_tokens": 1500,
                "total_costos": 0.025
            }
        }

class TaskCreateResponseSchema(BaseModel):
    """Schema Pydantic para respuesta de creación de tarea"""
    
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    data: TaskResponseSchema = Field(..., description="Tarea creada")
    message: str = Field(..., description="Mensaje de respuesta")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "id": 1,
                    "title": "Nueva tarea",
                    "description": "Descripción de la nueva tarea",
                    "priority": "media",
                    "effort": 4,
                    "status": "pendiente",
                    "assigned_to": "Ana García",
                    "assigned_role": "Técnico",
                    "category": "testing",
                    "created_at": "2024-01-15T10:30:00",
                    "updated_at": "2024-01-15T10:30:00",
                    "risk_analysis": None,
                    "mitigation_plan": None,
                    "tokens_gastados": 0,
                    "costos": 0.0
                },
                "message": "Tarea creada exitosamente"
            }
        }

class TaskUpdateResponseSchema(BaseModel):
    """Schema Pydantic para respuesta de actualización de tarea"""
    
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    data: TaskResponseSchema = Field(..., description="Tarea actualizada")
    message: str = Field(..., description="Mensaje de respuesta")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "id": 1,
                    "title": "Tarea actualizada",
                    "description": "Descripción actualizada",
                    "priority": "alta",
                    "effort": 6,
                    "status": "en_progreso",
                    "assigned_to": "Ana García",
                    "assigned_role": "Técnico",
                    "category": "testing",
                    "created_at": "2024-01-15T10:30:00",
                    "updated_at": "2024-01-15T11:30:00",
                    "risk_analysis": "Análisis actualizado",
                    "mitigation_plan": "Plan actualizado",
                    "tokens_gastados": 2000,
                    "costos": 0.035
                },
                "message": "Tarea actualizada exitosamente"
            }
        }

class TaskDeleteResponseSchema(BaseModel):
    """Schema Pydantic para respuesta de eliminación de tarea"""
    
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje de respuesta")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Tarea eliminada exitosamente"
            }
        } 