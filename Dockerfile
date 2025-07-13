# ==========================================
# DOCKERFILE SIMPLIFICADO PARA TASK MANAGER
# ==========================================

FROM python:3.9-slim

# Establecer variables de entorno para producción
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias
COPY task_manager/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY task_manager/ .

# Crear directorio para datos
RUN mkdir -p data logs

# Verificar que la aplicación puede importarse correctamente
RUN python -c "from app import create_app; print('✅ Application imports successfully')"

# Exponer el puerto 5000
EXPOSE 5000

# Healthcheck para verificar que la aplicación está funcionando
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/tasks || exit 1

# Comando para ejecutar la aplicación
CMD ["python", "run.py"] 