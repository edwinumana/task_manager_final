# ==========================================
# DOCKERFILE SIMPLIFICADO PARA TASK MANAGER
# ==========================================

FROM python:3.9-slim

# Establecer variables de entorno para producción
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Definir build args para las variables de entorno de Azure
ARG AZURE_MYSQL_CONNECTION_STRING
ARG AZURE_OPENAI_API_KEY
ARG AZURE_OPENAI_ENDPOINT
ARG AZURE_OPENAI_DEPLOYMENT_NAME
ARG AZURE_OPENAI_API_VERSION
ARG TEMPERATURE
ARG MAX_TOKENS
ARG TOP_P
ARG FREQUENCY_PENALTY
ARG PRESENCE_PENALTY

# Establecer variables de entorno desde build args
ENV AZURE_MYSQL_CONNECTION_STRING=${AZURE_MYSQL_CONNECTION_STRING}
ENV AZURE_OPENAI_API_KEY=${AZURE_OPENAI_API_KEY}
ENV AZURE_OPENAI_ENDPOINT=${AZURE_OPENAI_ENDPOINT}
ENV AZURE_OPENAI_DEPLOYMENT_NAME=${AZURE_OPENAI_DEPLOYMENT_NAME}
ENV AZURE_OPENAI_API_VERSION=${AZURE_OPENAI_API_VERSION}
ENV TEMPERATURE=${TEMPERATURE}
ENV MAX_TOKENS=${MAX_TOKENS}
ENV TOP_P=${TOP_P}
ENV FREQUENCY_PENALTY=${FREQUENCY_PENALTY}
ENV PRESENCE_PENALTY=${PRESENCE_PENALTY}

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