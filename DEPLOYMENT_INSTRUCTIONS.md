# 🚀 Instrucciones de Despliegue - Task Manager CI/CD

**Fuente**: Arial 12  
**Interlineado**: 1.5

## 📋 Guía Paso a Paso para Configurar el Pipeline

### **Prerrequisitos**

Antes de comenzar, asegúrate de tener:
- ✅ **Cuenta de GitHub** activa
- ✅ **Cuenta de Docker Hub** activa
- ✅ **Git** instalado localmente
- ✅ **Docker** instalado (opcional para pruebas locales)

---

## 🔧 Paso 1: Configurar Docker Hub

### **1.1 Crear Cuenta en Docker Hub**

1. Ir a [Docker Hub](https://hub.docker.com/)
2. Hacer clic en **Sign Up** si no tienes cuenta
3. Completar el registro con tu información

### **1.2 Generar Access Token**

1. Iniciar sesión en Docker Hub
2. Hacer clic en tu **nombre de usuario** (esquina superior derecha)
3. Seleccionar **Account Settings**
4. Ir a la pestaña **Security**
5. Hacer clic en **New Access Token**
6. Configurar el token:
   - **Token Description**: `GitHub Actions CI/CD`
   - **Permissions**: `Read, Write, Delete`
7. Hacer clic en **Generate**
8. **⚠️ IMPORTANTE**: Copiar el token inmediatamente (no se mostrará de nuevo)

### **1.3 Verificar Configuración**

```bash
# Probar login localmente (opcional)
docker login
# Introducir tu username y el access token como password
```

---

## 🐙 Paso 2: Crear Repositorio en GitHub

### **2.1 Crear Nuevo Repositorio**

1. Ir a [GitHub](https://github.com/)
2. Hacer clic en **New repository**
3. Configurar el repositorio:
   - **Repository name**: `task_manager_final`
   - **Description**: `Task Manager - Sistema de Gestión de Tareas con CI/CD`
   - **Visibility**: `Public`
   - **Initialize with README**: ❌ (No marcar)
4. Hacer clic en **Create repository**

### **2.2 Configurar Secretos del Repositorio**

1. En tu repositorio recién creado, ir a **Settings**
2. En el menú lateral, seleccionar **Secrets and variables** > **Actions**
3. Hacer clic en **New repository secret**
4. Agregar el primer secreto:
   - **Name**: `DOCKER_USERNAME`
   - **Secret**: Tu nombre de usuario de Docker Hub
   - Hacer clic en **Add secret**
5. Agregar el segundo secreto:
   - **Name**: `DOCKER_PASSWORD`
   - **Secret**: El access token generado en el paso 1.2
   - Hacer clic en **Add secret**

### **2.3 Verificar Secretos**

Deberías ver dos secretos configurados:
- ✅ `DOCKER_USERNAME`
- ✅ `DOCKER_PASSWORD`

---

## 📁 Paso 3: Preparar el Código

### **3.1 Clonar el Repositorio Local**

```bash
# Clonar tu repositorio vacío
git clone https://github.com/tu-usuario/task_manager_final.git
cd task_manager_final
```

### **3.2 Copiar Archivos de la Aplicación**

Copiar **SOLO** el contenido de la carpeta `m4_entregable4_V2_Edwin_Umaña_Peña` (sin la carpeta padre):

```bash
# Estructura que debes tener:
task_manager_final/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── task_manager/
│   ├── app/
│   ├── tests/
│   ├── config.py
│   ├── run.py
│   └── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
├── .dockerignore
└── DEPLOYMENT_INSTRUCTIONS.md
```

### **3.3 Verificar Archivos Críticos**

Asegúrate de que estos archivos estén presentes:
- ✅ `.github/workflows/ci-cd.yml` (Pipeline)
- ✅ `Dockerfile` (Imagen Docker)
- ✅ `task_manager/requirements.txt` (Dependencias)
- ✅ `task_manager/run.py` (Punto de entrada)
- ✅ `.dockerignore` (Optimización)

---

## 🚀 Paso 4: Ejecutar el Pipeline

### **4.1 Subir Código a GitHub**

```bash
# Agregar todos los archivos
git add .

# Crear commit inicial
git commit -m "Initial commit: Task Manager with CI/CD pipeline"

# Subir a GitHub (esto activará el pipeline)
git push origin main
```

### **4.2 Monitorear el Pipeline**

1. Ir a tu repositorio en GitHub
2. Hacer clic en la pestaña **Actions**
3. Deberías ver el pipeline ejecutándose: `🚀 Task Manager CI/CD Pipeline`
4. Hacer clic en el pipeline para ver los detalles

### **4.3 Verificar Etapas del Pipeline**

El pipeline ejecutará estas etapas en orden:

#### **Etapa 1: 🧪 Testing & Quality Checks**
- Tests unitarios
- Tests de integración  
- Tests core
- Reportes de cobertura

#### **Etapa 2: 🐳 Build Docker Image**
- Construcción de imagen
- Pruebas de salud
- Verificación de endpoints

#### **Etapa 3: 🚀 Push to Docker Hub**
- Autenticación con Docker Hub
- Generación de tags
- Subida de imagen

#### **Etapa 4: ✅ Verify Deployment**
- Descarga desde Docker Hub
- Verificación de funcionamiento

---

## 📊 Paso 5: Verificar el Despliegue

### **5.1 Verificar en Docker Hub**

1. Ir a [Docker Hub](https://hub.docker.com/)
2. Buscar: `tu-usuario/task-manager`
3. Verificar que la imagen esté disponible con los tags:
   - `latest`
   - SHA del commit
   - Número de versión (v1, v2, etc.)

### **5.2 Probar la Imagen Desplegada**

```bash
# Descargar y ejecutar la imagen
docker pull tu-usuario/task-manager:latest
docker run -p 5000:5000 tu-usuario/task-manager:latest

# Verificar que funciona
curl http://localhost:5000/tasks
```

### **5.3 Verificar Endpoints**

La aplicación debe responder en:
- ✅ `http://localhost:5000/tasks` (Página principal)
- ✅ `http://localhost:5000/user-stories` (Historias de usuario)
- ✅ `http://localhost:5000/tasks/api/list` (API de tareas)

---

## 🔄 Paso 6: Flujo de Trabajo Continuo

### **6.1 Desarrollo Iterativo**

```bash
# Hacer cambios en el código
# Ejemplo: editar task_manager/app/templates/base.html

# Commit y push (activará el pipeline automáticamente)
git add .
git commit -m "feat: improve UI design"
git push origin main
```

### **6.2 Monitoreo Continuo**

1. Cada push activará el pipeline automáticamente
2. Revisar la pestaña **Actions** para ver el estado
3. La imagen se actualizará automáticamente en Docker Hub

### **6.3 Versionado Automático**

El pipeline genera automáticamente:
- **Tag `latest`**: Última versión estable
- **Tag SHA**: Identificador único del commit
- **Tag versión**: Incremental (v1, v2, v3, etc.)

---

## 🛠️ Troubleshooting

### **Problemas Comunes**

#### **❌ Error: "Authentication failed"**
```
Error: denied: requested access to the resource is denied
```
**Solución:**
1. Verificar que `DOCKER_USERNAME` sea correcto
2. Regenerar access token en Docker Hub
3. Actualizar `DOCKER_PASSWORD` en GitHub Secrets

#### **❌ Error: "Tests failed"**
```
Error: process completed with exit code 1
```
**Solución:**
1. Revisar logs del pipeline en GitHub Actions
2. Ejecutar tests localmente: `cd task_manager && python -m pytest tests/ -v`
3. Corregir errores y hacer nuevo commit

#### **❌ Error: "Docker build failed"**
```
Error: failed to solve: process did not complete successfully
```
**Solución:**
1. Verificar que `Dockerfile` esté presente
2. Comprobar que `task_manager/requirements.txt` exista
3. Revisar logs de build en GitHub Actions

#### **❌ Error: "Health check failed"**
```
Error: Application failed to start
```
**Solución:**
1. Verificar que `task_manager/run.py` sea ejecutable
2. Comprobar dependencias en `requirements.txt`
3. Revisar logs del contenedor

### **Comandos de Debugging**

```bash
# Probar build local
docker build -t test-image .

# Probar ejecución local
docker run -p 5000:5000 test-image

# Ver logs del contenedor
docker logs [container-id]

# Ejecutar tests localmente
cd task_manager
python -m pytest tests/ -v --tb=short
```

---

## 📋 Checklist de Verificación

### **Antes del Despliegue**
- [ ] Cuenta de Docker Hub creada
- [ ] Access token generado
- [ ] Repositorio GitHub creado
- [ ] Secretos configurados correctamente
- [ ] Código copiado sin carpeta padre

### **Durante el Despliegue**
- [ ] Pipeline ejecutándose en GitHub Actions
- [ ] Todas las etapas completadas exitosamente
- [ ] Imagen subida a Docker Hub
- [ ] Tags generados correctamente

### **Después del Despliegue**
- [ ] Imagen disponible en Docker Hub
- [ ] Aplicación funciona localmente
- [ ] Endpoints responden correctamente
- [ ] Pipeline se ejecuta en nuevos commits

---

## 🎉 Conclusión

Si has seguido todos los pasos correctamente, deberías tener:

✅ **Pipeline CI/CD funcionando** en GitHub Actions  
✅ **Imagen Docker** disponible en Docker Hub  
✅ **Aplicación desplegada** y funcionando  
✅ **Actualizaciones automáticas** en cada commit  

### **Próximos Pasos**

1. **Personalizar**: Modificar la aplicación según tus necesidades
2. **Monitorear**: Revisar regularmente el estado del pipeline
3. **Escalar**: Considerar despliegue en producción con Kubernetes
4. **Mejorar**: Agregar más tests y funcionalidades

### **Enlaces Útiles**

- **Tu repositorio**: `https://github.com/tu-usuario/task_manager_final`
- **Docker Hub**: `https://hub.docker.com/r/tu-usuario/task-manager`
- **GitHub Actions**: `https://github.com/tu-usuario/task_manager_final/actions`

**¡Felicitaciones! Has configurado exitosamente un pipeline CI/CD completo.** 🚀 