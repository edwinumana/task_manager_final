# 🚀 Guía Completa de Despliegue - Task Manager CI/CD

## 📋 Índice

1. [Configuración Inicial](#configuración-inicial)
2. [Configuración de GitHub](#configuración-de-github)
3. [Configuración de Docker Hub](#configuración-de-docker-hub)
4. [Ejecución del Pipeline](#ejecución-del-pipeline)
5. [Verificación del Despliegue](#verificación-del-despliegue)
6. [Troubleshooting](#troubleshooting)
7. [Monitoreo y Mantenimiento](#monitoreo-y-mantenimiento)

---

## 🔧 Configuración Inicial

### **Prerrequisitos**

✅ **Cuenta de GitHub** activa con repositorio `task_manager`  
✅ **Cuenta de Docker Hub** con permisos de escritura  
✅ **Aplicación Task Manager** funcionando localmente  
✅ **Git** configurado con acceso al repositorio  

### **Estructura del Proyecto**

```
task_manager/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # Pipeline principal
├── task_manager/              # Código de la aplicación
├── Dockerfile                 # Imagen Docker optimizada
├── docker-compose.yml         # Orquestación local
├── README.md                  # Documentación principal
└── DEPLOYMENT_GUIDE.md        # Esta guía
```

---

## 🐙 Configuración de GitHub

### **1. Crear Repositorio**

```bash
# Inicializar repositorio local
git init
git add .
git commit -m "Initial commit: Task Manager application"

# Conectar con GitHub
git remote add origin https://github.com/edwinumana/task_manager.git
git branch -M main
git push -u origin main
```

### **2. Configurar Secretos**

#### **Acceder a la Configuración de Secretos:**

1. Ir a tu repositorio: `https://github.com/edwinumana/task_manager`
2. Navegar a **Settings** (Configuración)
3. En el menú lateral, seleccionar **Secrets and variables** > **Actions**
4. Hacer clic en **New repository secret**

#### **Secretos Requeridos:**

| Nombre | Valor | Descripción |
|--------|-------|-------------|
| `DOCKER_USERNAME` | `tu-usuario-dockerhub` | Usuario de Docker Hub |
| `DOCKER_PASSWORD` | `tu-token-dockerhub` | Token de acceso de Docker Hub |

**⚠️ Importante:** Usar un **Access Token** de Docker Hub, no tu contraseña personal.

### **3. Generar Token de Docker Hub**

1. Ir a [Docker Hub](https://hub.docker.com/)
2. Hacer clic en tu avatar > **Account Settings**
3. Seleccionar **Security** > **New Access Token**
4. Nombre: `GitHub-Actions-TaskManager`
5. Permisos: **Read, Write, Delete**
6. Copiar el token generado

---

## 🐳 Configuración de Docker Hub

### **1. Crear Repositorio**

1. Ir a [Docker Hub](https://hub.docker.com/)
2. Hacer clic en **Create Repository**
3. Nombre: `task-manager`
4. Visibilidad: **Public** (para facilitar el acceso)
5. Descripción: "Task Manager - Sistema de gestión de tareas con IA"

### **2. Verificar Configuración**

```bash
# Probar login local
docker login

# Verificar que puedes hacer push
docker build -t tu-usuario/task-manager:test .
docker push tu-usuario/task-manager:test
```

---

## 🔄 Ejecución del Pipeline

### **Triggers del Pipeline**

El pipeline se ejecuta automáticamente en:

- **Push** a `main`, `master`, o `develop`
- **Pull Request** a `main` o `master`
- **Ejecución manual** desde GitHub Actions

### **Ejecución Manual**

1. Ir a tu repositorio en GitHub
2. Navegar a **Actions**
3. Seleccionar **CI/CD Pipeline - Task Manager**
4. Hacer clic en **Run workflow**
5. Seleccionar la rama (por defecto `main`)
6. Hacer clic en **Run workflow**

### **Monitoreo en Tiempo Real**

```bash
# Ver el estado del pipeline
# Ir a: https://github.com/edwinumana/task_manager/actions

# O usar GitHub CLI
gh workflow list
gh run list
gh run view --web
```

---

## ✅ Verificación del Despliegue

### **1. Verificar Pipeline Completo**

#### **Etapa 1: Testing 🧪**
- ✅ Tests independientes ejecutados
- ✅ Tests de modelos ejecutados
- ✅ Artefactos de testing subidos

#### **Etapa 2: Build 🐳**
- ✅ Imagen Docker construida
- ✅ Health check pasado
- ✅ Imagen guardada como artefacto

#### **Etapa 3: Push 🚀**
- ✅ Login a Docker Hub exitoso
- ✅ Tags generados correctamente
- ✅ Imágenes subidas a Docker Hub

#### **Etapa 4: Verification ✅**
- ✅ Imagen descargada desde Docker Hub
- ✅ Contenedor desplegado correctamente
- ✅ Aplicación funcionando

### **2. Verificar Imagen en Docker Hub**

```bash
# Verificar que la imagen existe
docker search tu-usuario/task-manager

# Descargar y probar la imagen
docker pull tu-usuario/task-manager:latest
docker run -p 5000:5000 tu-usuario/task-manager:latest
```

### **3. Verificar Aplicación**

```bash
# Probar endpoints principales
curl http://localhost:5000/tasks
curl http://localhost:5000/user-stories

# Verificar health check
curl -f http://localhost:5000/tasks || echo "Health check failed"
```

### **4. Verificar Tags**

Las siguientes etiquetas deben estar disponibles:

- `latest` - Última versión estable
- `<commit-sha>` - Versión específica del commit
- `<timestamp>` - Versión con timestamp

```bash
# Verificar tags disponibles
docker pull tu-usuario/task-manager:latest
docker pull tu-usuario/task-manager:abc1234  # Ejemplo de SHA
```

---

## 🔧 Troubleshooting

### **Problemas Comunes**

#### **1. Error de Autenticación con Docker Hub**

**Síntoma:**
```
Error: denied: requested access to the resource is denied
```

**Solución:**
```bash
# Verificar secretos en GitHub
# Settings > Secrets > Actions
# Asegurar que DOCKER_USERNAME y DOCKER_PASSWORD están configurados

# Verificar token de Docker Hub
docker login -u tu-usuario -p tu-token
```

#### **2. Fallos en Tests**

**Síntoma:**
```
pytest tests/test_core_isolated.py FAILED
```

**Solución:**
```bash
# Ejecutar tests localmente
cd task_manager
python -m pytest tests/test_core_isolated.py -v

# Revisar dependencias
pip install -r requirements.txt
```

#### **3. Error de Build de Docker**

**Síntoma:**
```
ERROR: failed to solve: process "/bin/sh -c python -c ..." did not complete successfully
```

**Solución:**
```bash
# Probar build local
docker build -t task-manager .

# Verificar Dockerfile
docker build --no-cache -t task-manager .
```

#### **4. Health Check Fallando**

**Síntoma:**
```
Health check failed: curl -f http://localhost:5000/tasks
```

**Solución:**
```bash
# Verificar que la aplicación inicia correctamente
docker run -p 5000:5000 task-manager
docker logs container-name

# Verificar puerto y endpoint
curl -v http://localhost:5000/tasks
```

### **Logs de Depuración**

```bash
# Ver logs del pipeline en GitHub Actions
# https://github.com/edwinumana/task_manager/actions

# Ver logs de contenedor local
docker logs -f container-name

# Acceder al contenedor para debug
docker exec -it container-name /bin/bash
```

---

## 📊 Monitoreo y Mantenimiento

### **Métricas del Pipeline**

#### **Tiempos de Ejecución Típicos:**
- **Testing**: 3-5 minutos
- **Build**: 2-4 minutos
- **Push**: 1-3 minutos
- **Verification**: 1-2 minutos
- **Total**: 7-14 minutos

#### **Uso de Recursos:**
- **GitHub Actions**: ~15 minutos por ejecución
- **Docker Hub**: ~100MB por imagen
- **Almacenamiento**: ~500MB total

### **Monitoreo Automatizado**

```bash
# Script de monitoreo (opcional)
#!/bin/bash
# monitor-deployment.sh

DOCKER_IMAGE="tu-usuario/task-manager:latest"
CONTAINER_NAME="task-manager-monitor"

echo "🔍 Verificando imagen en Docker Hub..."
docker pull $DOCKER_IMAGE

echo "🚀 Iniciando contenedor de prueba..."
docker run -d --name $CONTAINER_NAME -p 5001:5000 $DOCKER_IMAGE

echo "⏳ Esperando inicio de aplicación..."
sleep 10

echo "🧪 Probando aplicación..."
if curl -f http://localhost:5001/tasks; then
    echo "✅ Aplicación funcionando correctamente"
else
    echo "❌ Error en la aplicación"
fi

echo "🛑 Limpiando contenedor de prueba..."
docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME
```

### **Mantenimiento Regular**

#### **Semanal:**
- Revisar logs de pipeline
- Verificar uso de cuota de GitHub Actions
- Limpiar imágenes antiguas de Docker Hub

#### **Mensual:**
- Actualizar dependencias de Python
- Revisar y actualizar secretos
- Optimizar Dockerfile si es necesario

#### **Comandos de Limpieza:**

```bash
# Limpiar imágenes locales
docker system prune -a

# Limpiar artefactos de GitHub Actions (manual)
# Settings > Actions > General > Artifact and log retention

# Limpiar tags antiguos de Docker Hub (manual)
# Hub.docker.com > Repository > Tags > Delete
```

---

## 🎯 Checklist de Verificación Completa

### **Pre-Despliegue**
- [ ] Repositorio GitHub configurado
- [ ] Secretos de Docker Hub configurados
- [ ] Pipeline `.github/workflows/ci-cd.yml` presente
- [ ] Dockerfile optimizado
- [ ] Tests pasando localmente

### **Durante el Despliegue**
- [ ] Pipeline ejecutándose sin errores
- [ ] Etapa de testing completada
- [ ] Imagen Docker construida
- [ ] Push a Docker Hub exitoso
- [ ] Verificación final pasada

### **Post-Despliegue**
- [ ] Imagen disponible en Docker Hub
- [ ] Aplicación funcionando al descargar imagen
- [ ] Endpoints respondiendo correctamente
- [ ] Logs sin errores críticos
- [ ] Documentación actualizada

---

## 📞 Soporte y Contacto

### **Recursos de Ayuda**

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Docker Hub Docs**: https://docs.docker.com/docker-hub/
- **Flask Deployment**: https://flask.palletsprojects.com/en/2.0.x/deploying/

### **Contacto**

- **Desarrollador**: Edwin Umaña Peña
- **Email**: edwin.umanha@gmail.com
- **Repository**: https://github.com/edwinumana/task_manager
- **Issues**: https://github.com/edwinumana/task_manager/issues

---

## 🎉 ¡Felicitaciones!

Si has llegado hasta aquí y todos los checks están ✅, has configurado exitosamente:

🚀 **Pipeline CI/CD completo con GitHub Actions**  
🐳 **Despliegue automatizado a Docker Hub**  
🧪 **Testing automatizado con pytest**  
📦 **Imagen Docker optimizada para producción**  
🔄 **Proceso de verificación y validación**  

**Tu aplicación Task Manager está ahora lista para producción con CI/CD automatizado.**

---

**© 2024 Edwin Umaña Peña - Task Manager Deployment Guide** 