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

## 🐳 Instrucciones para Ejecutar la Imagen Docker

### **Requisitos Previos**

- Docker instalado en tu sistema
- Conexión a internet para descargar la imagen

### **Opción 1: Ejecutar desde Docker Hub (Recomendado)**

```bash
# 1. Descargar la imagen desde Docker Hub
docker pull melquiadescontenidos/task-manager-app:latest

# 2. Ejecutar la aplicación
docker run -d --name task-manager \
  -p 5000:5000 \
  -e AZURE_MYSQL_CONNECTION_STRING="tu_connection_string" \
  -e AZURE_OPENAI_API_KEY="tu_api_key" \
  -e AZURE_OPENAI_ENDPOINT="tu_endpoint" \
  -e AZURE_OPENAI_DEPLOYMENT_NAME="tu_deployment" \
  -e AZURE_OPENAI_API_VERSION="2023-12-01-preview" \
  -e TEMPERATURE="0.7" \
  -e MAX_TOKENS="150" \
  -e TOP_P="0.9" \
  -e FREQUENCY_PENALTY="0.0" \
  -e PRESENCE_PENALTY="0.0" \
  melquiadescontenidos/task-manager-app:latest
```

### **Opción 2: Ejecutar con Docker Compose**

```bash
# 1. Clonar el repositorio
git clone https://github.com/edwinumana/task_manager_final.git
cd task_manager_final

# 2. Configurar variables de entorno (opcional)
# Crear archivo .env con tus credenciales de Azure

# 3. Ejecutar con docker-compose
docker-compose up -d
```

### **Opción 3: Construir Localmente**

```bash
# 1. Clonar el repositorio
git clone https://github.com/edwinumana/task_manager_final.git
cd task_manager_final

# 2. Construir la imagen
docker build -t task-manager-local .

# 3. Ejecutar la aplicación
docker run -d --name task-manager-local \
  -p 5000:5000 \
  -e AZURE_MYSQL_CONNECTION_STRING="tu_connection_string" \
  -e AZURE_OPENAI_API_KEY="tu_api_key" \
  -e AZURE_OPENAI_ENDPOINT="tu_endpoint" \
  -e AZURE_OPENAI_DEPLOYMENT_NAME="tu_deployment" \
  -e AZURE_OPENAI_API_VERSION="2023-12-01-preview" \
  -e TEMPERATURE="0.7" \
  -e MAX_TOKENS="150" \
  -e TOP_P="0.9" \
  -e FREQUENCY_PENALTY="0.0" \
  -e PRESENCE_PENALTY="0.0" \
  task-manager-local
```

### **Verificar que la Aplicación Funciona**

```bash
# Verificar que el contenedor está ejecutándose
docker ps

# Probar los endpoints principales
curl http://localhost:5000/tasks
curl http://localhost:5000/user-stories

# Ver logs del contenedor
docker logs task-manager
```

### **Acceder a la Aplicación**

Una vez ejecutada, la aplicación estará disponible en:
- **URL Principal**: http://localhost:5000
- **API Tasks**: http://localhost:5000/tasks
- **API User Stories**: http://localhost:5000/user-stories

---

## 🔐 Configuración de Variables de Entorno

### **Variables Requeridas para Azure OpenAI**

```bash
AZURE_OPENAI_API_KEY=tu_api_key_de_azure
AZURE_OPENAI_ENDPOINT=https://tu-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=tu_deployment_name
AZURE_OPENAI_API_VERSION=2023-12-01-preview
```

### **Variables Requeridas para Azure MySQL**

```bash
AZURE_MYSQL_CONNECTION_STRING=mysql://usuario:contraseña@servidor:puerto/base_datos
```

### **Variables Opcionales para el Modelo IA**

```bash
TEMPERATURE=0.7
MAX_TOKENS=150
TOP_P=0.9
FREQUENCY_PENALTY=0.0
PRESENCE_PENALTY=0.0
```

---

## 📊 Funcionalidades de la Aplicación

### **Gestión de Tareas**
- ✅ Crear, leer, actualizar y eliminar tareas
- ✅ Asignar prioridades y estados
- ✅ Categorización automática con IA
- ✅ Estimación de esfuerzo inteligente
- ✅ Análisis de riesgos automatizado

### **Historias de Usuario**
- ✅ Crear y gestionar historias de usuario
- ✅ Estimación de puntos de historia
- ✅ Conversión automática a horas
- ✅ Seguimiento de progreso

### **Inteligencia Artificial**
- ✅ Generación automática de descripciones
- ✅ Categorización inteligente de tareas
- ✅ Estimación de esfuerzo basada en IA
- ✅ Análisis de riesgos automatizado
- ✅ Sugerencias de mejora

### **Estadísticas y Reportes**
- ✅ Dashboard con métricas en tiempo real
- ✅ Gráficos de distribución de tareas
- ✅ Análisis de productividad
- ✅ Reportes de progreso

---

## 🧪 Testing y Calidad

### **Suite de Pruebas**
- **35 tests automatizados** con pytest
- **94.3% de éxito** en ejecución
- **Tests unitarios** para modelos y controladores
- **Tests de integración** para endpoints
- **Tests de funcionalidad core**

### **Cobertura de Código**
- Reportes de cobertura automáticos
- Verificación de calidad de código
- Validación de endpoints principales

---

## 🔗 Enlaces del Proyecto

### **Repositorio Público en GitHub**
- **URL**: https://github.com/edwinumana/task_manager_final
- **Pipeline CI/CD**: https://github.com/edwinumana/task_manager_final/actions
- **Docker Hub**: https://hub.docker.com/r/melquiadescontenidos/task-manager-app

### **Archivos Principales**
- **Pipeline CI/CD**: `.github/workflows/ci-cd.yml`
- **Dockerfile**: `Dockerfile`
- **README**: `README.md`

---

## 👥 Autores

**Desarrollado por**: Edwin Umaña Peña  
**Universidad**: UNIR  
**Curso**: Programación con IA  
**Entregable**: M4 - Entregable 4

---

## 📄 Licencia

Este proyecto está desarrollado como parte del curso de Programación con IA de la UNIR. Todos los derechos reservados.

---

## 🤝 Contribuciones

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

---

## 📞 Soporte

Para soporte técnico o preguntas sobre el proyecto:
- **Email**: edwin.umana@unir.net
- **GitHub Issues**: https://github.com/edwinumana/task_manager_final/issues