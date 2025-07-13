# 🚀 Task Manager - Sistema de Gestión de Tareas con IA

**Fuente**: Arial 12  
**Interlineado**: 1.5

## 📋 Descripción del Proyecto

**Task Manager** es una aplicación web empresarial desarrollada en **Flask** que permite la gestión completa de tareas a partir de historias de usuario, integrada con **Azure OpenAI** para automatización inteligente y análisis de riesgos. La aplicación está completamente containerizada con **Docker** y cuenta con un pipeline de **CI/CD** automatizado usando **GitHub Actions**.

### 🎯 Características Principales

- **Gestión Completa de Tareas**: CRUD completo con 23 endpoints activos
- **Inteligencia Artificial**: Integración con Azure OpenAI para generación automática de descripciones, categorización, estimación de esfuerzo y análisis de riesgos
- **Historias de Usuario**: Metodología ágil con puntos de historia y estimación de horas
- **Base de Datos Híbrida**: Soporte para Azure MySQL con fallback a JSON
- **Interfaz Responsiva**: Bootstrap 5 con gráficos estadísticos usando Chart.js
- **Sistema de Testing**: 35 tests automatizados con pytest (94.3% de éxito)
- **Containerización**: Docker multi-stage optimizado para producción
- **CI/CD Automatizado**: Pipeline completo con GitHub Actions y Docker Hub

---

## 🏗️ Arquitectura de la Aplicación

### **Estructura de Directorios**

```
task_manager/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # Pipeline CI/CD automatizado
├── app/
│   ├── controllers/           # Lógica de negocio
│   ├── database/             # Conexión y migraciones BD
│   ├── models/               # Modelos de datos
│   ├── routes/               # Rutas/endpoints
│   ├── schemas/              # Esquemas de validación
│   ├── services/             # Servicios (IA, etc.)
│   ├── templates/            # Plantillas HTML
│   └── utils/                # Utilidades
├── tests/                    # Suite de pruebas automatizadas
├── config.py                 # Configuración
├── run.py                    # Punto de entrada
├── requirements.txt          # Dependencias
├── Dockerfile               # Imagen Docker optimizada
├── docker-compose.yml       # Orquestación local
└── .dockerignore           # Optimización de build
```

### **Componentes Principales**

#### **1. Modelos de Datos**
- **Task**: Modelo principal de tareas
- **UserStory**: Historias de usuario (metodología ágil)
- **TaskDB/UserStoryDB**: Modelos para base de datos

#### **2. Controladores**
- **TaskController**: CRUD de tareas + funciones de IA
- **UserStoryController**: Gestión de historias de usuario
- **AIController**: Servicios de inteligencia artificial

#### **3. Rutas/Endpoints**
- **task_routes**: API REST para tareas
- **user_story_routes**: API para historias de usuario
- **ai_routes**: Endpoints específicos de IA

---

## 🔧 Tecnologías Utilizadas

### **Backend**
- **Flask 2.0.1**: Framework web principal
- **SQLAlchemy 1.4.23**: ORM para base de datos
- **Azure OpenAI**: Servicios de inteligencia artificial
- **Azure MySQL**: Base de datos principal
- **Pydantic 2.5.0**: Validación de datos

### **Frontend**
- **Bootstrap 5**: Framework CSS responsivo
- **Chart.js**: Gráficos estadísticos
- **JavaScript ES6+**: Interactividad
- **AJAX/Fetch**: Comunicación asíncrona

### **DevOps**
- **Docker**: Containerización
- **Docker Compose**: Orquestación local
- **GitHub Actions**: CI/CD Pipeline automatizado
- **Docker Hub**: Registro de imágenes
- **pytest**: Testing automatizado

---

## 🚀 Pipeline CI/CD Automatizado

### **🔄 Flujo del Pipeline**

El pipeline se ejecuta automáticamente en:
- **Push** a las ramas `main`, `master`, `develop`
- **Pull Request** a `main` o `master`
- **Ejecución manual** desde GitHub Actions

### **📋 Etapas del Pipeline**

#### **1. 🧪 Testing & Quality Checks**
```yaml
- Tests unitarios con pytest
- Tests de integración
- Tests de funcionalidad core
- Generación de reportes de cobertura
- Verificación de calidad de código
```

#### **2. 🐳 Build Docker Image**
```yaml
- Construcción de imagen Docker optimizada
- Pruebas de salud del contenedor
- Verificación de endpoints principales
- Guardado de imagen como artefacto
```

#### **3. 🚀 Push to Docker Hub**
```yaml
- Autenticación con Docker Hub
- Generación de tags automáticos:
  - latest
  - SHA del commit
  - Número de build (v1, v2, etc.)
- Subida a Docker Hub
```

#### **4. ✅ Deployment Verification**
```yaml
- Descarga de imagen desde Docker Hub
- Pruebas de despliegue en contenedor
- Verificación de funcionamiento
- Confirmación de disponibilidad
```

---

## 🔐 Configuración de Secretos de Docker Hub

### **Paso 1: Obtener Credenciales de Docker Hub**

1. Crear cuenta en [Docker Hub](https://hub.docker.com/)
2. Ir a **Account Settings** > **Security**
3. Crear un **Access Token** con permisos de escritura
4. Copiar el token generado

### **Paso 2: Configurar Secretos en GitHub**

1. Ir a tu repositorio en GitHub
2. Navegar a **Settings** > **Secrets and variables** > **Actions**
3. Hacer clic en **New repository secret**
4. Agregar los siguientes secretos:

```
DOCKER_USERNAME: tu-usuario-docker-hub
DOCKER_PASSWORD: tu-access-token-docker-hub
```

### **Paso 3: Verificar Configuración**

El pipeline verificará automáticamente la configuración en la primera ejecución.

---

## 🐳 Instrucciones de Despliegue

### **Opción 1: Usar Imagen desde Docker Hub (Recomendado)**

```bash
# Descargar y ejecutar la imagen más reciente
docker pull edwinumana/task-manager:latest
docker run -p 5000:5000 edwinumana/task-manager:latest

# O usar docker-compose
curl -o docker-compose.yml https://raw.githubusercontent.com/tu-usuario/task_manager_final/main/docker-compose.yml
docker-compose up -d
```

### **Opción 2: Construir Localmente**

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/task_manager_final.git
cd task_manager_final

# Construir y ejecutar con Docker Compose
docker-compose up --build -d
```

### **Opción 3: Desarrollo Local**

```bash
# Instalar dependencias
cd task_manager
pip install -r requirements.txt

# Ejecutar aplicación
python run.py
```

### **Acceso a la Aplicación**

Una vez desplegada, la aplicación estará disponible en:
- **URL**: http://localhost:5000
- **Puerto**: 5000

---

## 🧪 Sistema de Testing Automatizado

### **Estadísticas de Testing**
- **Total de tests**: 35
- **Tests exitosos**: 33
- **Tasa de éxito**: 94.3%
- **Cobertura**: Tests independientes al 100%

### **Categorías de Tests**
- **Tests unitarios**: Funcionalidad individual de componentes
- **Tests de integración**: Interacción entre componentes
- **Tests core**: Funcionalidad básica independiente
- **Tests de IA**: Servicios de inteligencia artificial
- **Tests de base de datos**: Operaciones CRUD

### **Ejecutar Tests Localmente**

```bash
# Tests completos
cd task_manager
python -m pytest tests/ -v

# Tests específicos por categoría
python -m pytest tests/ -m "unit" -v          # Solo tests unitarios
python -m pytest tests/ -m "integration" -v   # Solo tests de integración
python -m pytest tests/ -m "core" -v          # Solo tests core

# Tests con cobertura
python -m pytest tests/ --cov=app --cov-report=html
```

### **Integración con CI/CD**

Los tests se ejecutan automáticamente en el pipeline:
- **Tests unitarios**: Verifican funcionalidad individual
- **Tests de integración**: Prueban interacción entre componentes
- **Tests core**: Validan funcionalidad básica
- **Reportes de cobertura**: Generados automáticamente

---

## 🌐 Funcionalidades Principales

### **Gestión de Tareas**
- **CRUD Completo**: Crear, leer, actualizar, eliminar tareas
- **Estados**: Pendiente, En Progreso, En Revisión, Completada
- **Prioridades**: Baja, Media, Alta, Bloqueante
- **Categorización**: 15 categorías especializadas

### **Inteligencia Artificial**
- **Generación Automática**: Descripciones inteligentes
- **Categorización**: Clasificación automática por tipo
- **Estimación**: Cálculo de horas de esfuerzo
- **Análisis de Riesgos**: Identificación de riesgos potenciales
- **Planes de Mitigación**: Estrategias de reducción de riesgos

### **Historias de Usuario**
- **Metodología Ágil**: Gestión completa de user stories
- **Puntos de Historia**: Estimación ágil
- **Generación de Tareas**: Creación automática desde historias
- **Trazabilidad**: Relación entre historias y tareas

### **Estadísticas y Reportes**
- **Dashboard**: Visualización de métricas clave
- **Gráficos**: Distribución por estado, categoría, prioridad
- **Análisis**: Tendencias y patrones de trabajo
- **Exportación**: Datos en formato JSON

---

## 📊 Monitoreo y Mantenimiento

### **Health Checks**
- **Endpoint de salud**: `/tasks` para verificar disponibilidad
- **Docker Health Check**: Verificación automática del contenedor
- **Pipeline Verification**: Validación post-despliegue

### **Logs y Debugging**
```bash
# Ver logs del contenedor
docker logs [container-name]

# Acceder al contenedor para debugging
docker exec -it [container-name] /bin/bash

# Verificar estado del pipeline
# Revisar en GitHub Actions > tu-repositorio > Actions
```

### **Actualizaciones Automáticas**
- **Trigger automático**: Push a rama principal
- **Versionado**: Tags automáticos con SHA y número de build
- **Rollback**: Usar tags específicos para volver a versiones anteriores

---

## 🔧 Configuración Avanzada

### **Variables de Entorno**

```env
# Configuración básica
SECRET_KEY=tu-clave-secreta-aqui
FLASK_ENV=production

# Azure OpenAI (opcional)
AZURE_OPENAI_API_KEY=tu-api-key
AZURE_OPENAI_ENDPOINT=tu-endpoint
AZURE_OPENAI_API_VERSION=2023-05-15
AZURE_OPENAI_DEPLOYMENT_NAME=tu-deployment

# Azure MySQL (opcional)
AZURE_MYSQL_CONNECTION_STRING=tu-connection-string
AZURE_MYSQL_SSL_CA=path-to-ca-cert
AZURE_MYSQL_SSL_VERIFY=true
```

### **Configuración de Docker Compose**

```yaml
# docker-compose.yml personalizado
services:
  task-manager:
    image: edwinumana/task-manager:latest
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

---

## 🚀 Despliegue en Producción

### **Recomendaciones**
1. **Usar tags específicos** en lugar de `latest` para producción
2. **Configurar variables de entorno** apropiadas
3. **Implementar monitoreo** y alertas
4. **Configurar backup** de datos
5. **Usar HTTPS** con certificados SSL

### **Ejemplo de Despliegue**
```bash
# Despliegue con tag específico
docker run -d \
  --name task-manager-prod \
  -p 80:5000 \
  -e SECRET_KEY=tu-clave-secreta-produccion \
  -e FLASK_ENV=production \
  -v /opt/task-manager/data:/app/data \
  --restart unless-stopped \
  edwinumana/task-manager:v123
```

---

## 📞 Soporte y Contribución

### **Reportar Issues**
- Usar el sistema de Issues de GitHub
- Incluir logs y pasos para reproducir
- Especificar versión de la imagen Docker

### **Contribuir**
1. Fork del repositorio
2. Crear rama para feature/bugfix
3. Ejecutar tests localmente
4. Enviar Pull Request
5. El pipeline validará automáticamente los cambios

### **Recursos Adicionales**
- **Docker Hub**: https://hub.docker.com/r/edwinumana/task-manager
- **GitHub Actions**: Revisar en la pestaña Actions del repositorio
- **Documentación**: Archivos README en subdirectorios

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 🎉 Conclusión

**Task Manager** es una aplicación completa y robusta que combina:
- ✅ **Desarrollo moderno** con Flask y Python
- ✅ **Inteligencia Artificial** con Azure OpenAI
- ✅ **Containerización** con Docker
- ✅ **CI/CD automatizado** con GitHub Actions
- ✅ **Testing automatizado** con pytest
- ✅ **Despliegue simplificado** con Docker Hub

**¡Listo para usar en producción!** 🚀