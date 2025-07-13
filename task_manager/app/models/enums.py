from enum import Enum

class TaskCategory(Enum):
    """
    Enum que define las categorías posibles para una tarea en un laboratorio
    de control de calidad farmacéutico
    """
    TESTING = "testing"  # Pruebas de calidad y control
    FRONTEND = "frontend"  # Desarrollo de interfaces de usuario
    BACKEND = "backend"  # Desarrollo de sistemas backend
    DESARROLLO = "desarrollo"  # Desarrollo general de software
    DISEÑO = "diseño"  # Diseño de sistemas y procesos
    DOCUMENTACION = "documentacion"  # Documentación técnica y procedimental
    BASE_DE_DATOS = "base_de_datos"  # Gestión y mantenimiento de bases de datos
    SEGURIDAD = "seguridad"  # Seguridad de sistemas y datos
    INFRAESTRUCTURA = "infraestructura"  # Infraestructura tecnológica
    MANTENIMIENTO = "mantenimiento"  # Mantenimiento de equipos y sistemas
    INVESTIGACION = "investigacion"  # Investigación y desarrollo
    SUPERVISION = "supervision"  # Supervisión de procesos y personal
    RIESGOS_LABORALES = "riesgos_laborales"  # Gestión de riesgos laborales
    LIMPIEZA = "limpieza"  # Limpieza y mantenimiento de áreas
    OTRO = "otro"  # Categoría por defecto para casos no especificados

    @classmethod
    def get_values(cls):
        """Retorna una lista de todos los valores posibles"""
        return [category.value for category in cls]

    @classmethod
    def get_display_names(cls):
        """Retorna un diccionario con los valores y sus nombres de visualización"""
        return {
            cls.TESTING.value: "Testing y Control de Calidad",
            cls.FRONTEND.value: "Desarrollo Frontend",
            cls.BACKEND.value: "Desarrollo Backend",
            cls.DESARROLLO.value: "Desarrollo General",
            cls.DISEÑO.value: "Diseño de Sistemas",
            cls.DOCUMENTACION.value: "Documentación",
            cls.BASE_DE_DATOS.value: "Base de Datos",
            cls.SEGURIDAD.value: "Seguridad",
            cls.INFRAESTRUCTURA.value: "Infraestructura",
            cls.MANTENIMIENTO.value: "Mantenimiento",
            cls.INVESTIGACION.value: "Investigación",
            cls.SUPERVISION.value: "Supervisión",
            cls.RIESGOS_LABORALES.value: "Riesgos Laborales",
            cls.LIMPIEZA.value: "Limpieza",
            cls.OTRO.value: "Otro"
        }

class PriorityEnum(str, Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    BLOQUEANTE = "bloqueante" 