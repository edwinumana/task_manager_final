# 🚀 EJECUTAR PASOS COMPLETOS - TASK MANAGER CI/CD

**Fuente**: Arial 12  
**Interlineado**: 1.5

## 📋 Guía de Ejecución Paso a Paso

### **🎯 OBJETIVO**
Implementar completamente el pipeline CI/CD para Task Manager con GitHub Actions y Docker Hub.

---

## **PASO 1: 🐙 CREAR REPOSITORIO GITHUB**

### **Instrucciones Detalladas:**

1. **Abrir GitHub**
   - Ir a [GitHub.com](https://github.com)
   - Iniciar sesión con tu cuenta

2. **Crear Nuevo Repositorio**
   - Hacer clic en **"New"** (botón verde) o **"+"** → **"New repository"**

3. **Configurar Repositorio**
   ```
   Repository name: task_manager_final
   Description: Task Manager - Sistema de Gestión de Tareas con CI/CD Pipeline
   Visibility: ✅ Public (OBLIGATORIO)
   Initialize with README: ❌ NO marcar
   Add .gitignore: ❌ NO seleccionar  
   Choose a license: ❌ NO seleccionar
   ```

4. **Crear y Copiar URL**
   - Hacer clic en **"Create repository"**
   - Copiar la URL que aparece (algo como: `https://github.com/TU-USUARIO/task_manager_final.git`)

### **✅ Verificación Paso 1:**
- [ ] Repositorio creado
- [ ] URL copiada
- [ ] Repositorio está vacío

---

## **PASO 2: 🔐 CONFIGURAR SECRETOS DOCKER HUB**

### **PARTE A: Obtener Credenciales Docker Hub**

1. **Ir a Docker Hub**
   - Abrir [Docker Hub](https://hub.docker.com/)
   - Iniciar sesión o crear cuenta

2. **Generar Access Token**
   - Hacer clic en tu **nombre de usuario** (esquina superior derecha)
   - **"Account Settings"** → **"Security"** → **"New Access Token"**
   - Configurar:
     ```
     Token Description: GitHub Actions CI/CD
     Permissions: ✅ Read, Write, Delete
     ```
   - **"Generate"** → **COPIAR TOKEN INMEDIATAMENTE**

### **PARTE B: Configurar Secretos en GitHub**

1. **Ir a tu repositorio `task_manager_final`**
2. **"Settings"** → **"Secrets and variables"** → **"Actions"**
3. **Agregar primer secreto:**
   - **"New repository secret"**
   - Name: `DOCKER_USERNAME`
   - Secret: `tu-nombre-usuario-docker-hub`
   - **"Add secret"**

4. **Agregar segundo secreto:**
   - **"New repository secret"**
   - Name: `DOCKER_PASSWORD`
   - Secret: `el-access-token-copiado`
   - **"Add secret"**

### **✅ Verificación Paso 2:**
- [ ] Access token generado
- [ ] DOCKER_USERNAME configurado
- [ ] DOCKER_PASSWORD configurado
- [ ] Ambos secretos aparecen en la lista

---

## **PASO 3: 📁 PREPARAR Y SUBIR ARCHIVOS**

### **Opción A: Automática (Recomendada)**

**Ejecutar el script de subida automática:**

```bash
python upload_to_github.py
```

**El script te pedirá:**
1. URL del repositorio GitHub (la que copiaste en Paso 1)
2. Mensaje del commit (opcional)
3. Confirmación para proceder

### **Opción B: Manual**

**Si prefieres hacerlo manualmente:**

```bash
# 1. Inicializar Git
git init

# 2. Configurar usuario (si no está configurado)
git config user.name "Tu Nombre"
git config user.email "tu-email@example.com"

# 3. Agregar archivos
git add .

# 4. Hacer commit
git commit -m "Initial commit: Task Manager with CI/CD pipeline"

# 5. Agregar remote
git remote add origin https://github.com/TU-USUARIO/task_manager_final.git

# 6. Configurar rama principal
git branch -M main

# 7. Subir a GitHub
git push -u origin main
```

### **✅ Verificación Paso 3:**
- [ ] Archivos subidos a GitHub
- [ ] Repositorio contiene todos los archivos
- [ ] Pipeline CI/CD presente en `.github/workflows/ci-cd.yml`

---

## **PASO 4: 🚀 VERIFICAR PIPELINE EN ACCIÓN**

### **Monitorear el Pipeline:**

1. **Ir a tu repositorio en GitHub**
2. **Hacer clic en la pestaña "Actions"**
3. **Deberías ver:** `🚀 Task Manager CI/CD Pipeline` ejecutándose

### **Etapas del Pipeline:**

#### **🧪 Testing & Quality Checks** (3-5 minutos)
- Tests unitarios
- Tests de integración
- Tests core
- Reportes de cobertura

#### **🐳 Build Docker Image** (5-8 minutos)
- Construcción de imagen
- Verificación de salud
- Pruebas de endpoints

#### **🚀 Push to Docker Hub** (2-3 minutos)
- Autenticación con Docker Hub
- Generación de tags
- Subida de imagen

#### **✅ Verify Deployment** (2-3 minutos)
- Descarga desde Docker Hub
- Verificación de funcionamiento

### **✅ Verificación Paso 4:**
- [ ] Pipeline ejecutándose sin errores
- [ ] Todas las etapas completadas (✅)
- [ ] No hay errores rojos (❌)

---

## **PASO 5: 🐳 VERIFICAR DESPLIEGUE EN DOCKER HUB**

### **Verificar Imagen en Docker Hub:**

1. **Ir a [Docker Hub](https://hub.docker.com/)**
2. **Buscar:** `tu-usuario/task-manager`
3. **Verificar que existe la imagen con tags:**
   - `latest`
   - SHA del commit
   - Número de versión (`v1`, `v2`, etc.)

### **Probar la Imagen:**

```bash
# Descargar y ejecutar
docker pull tu-usuario/task-manager:latest
docker run -p 5000:5000 tu-usuario/task-manager:latest

# En otra terminal, probar
curl http://localhost:5000/tasks
```

### **✅ Verificación Paso 5:**
- [ ] Imagen disponible en Docker Hub
- [ ] Tags generados correctamente
- [ ] Aplicación funciona al ejecutar la imagen
- [ ] Endpoints responden correctamente

---

## **🎉 RESULTADO FINAL**

### **¡FELICITACIONES! Has completado exitosamente:**

✅ **Pipeline CI/CD funcionando** - GitHub Actions ejecutándose automáticamente  
✅ **Testing automatizado** - 35 tests ejecutándose en cada commit  
✅ **Build automatizado** - Imagen Docker construyéndose automáticamente  
✅ **Despliegue automatizado** - Imagen subiendo a Docker Hub automáticamente  
✅ **Verificación automatizada** - Health checks y pruebas de endpoints  

### **🔄 Flujo Continuo:**
- Cada `git push` activará el pipeline automáticamente
- Los tests se ejecutarán en paralelo
- La imagen se actualizará en Docker Hub
- Todo el proceso es completamente automatizado

### **📊 Monitoreo Continuo:**
- **GitHub Actions**: `https://github.com/tu-usuario/task_manager_final/actions`
- **Docker Hub**: `https://hub.docker.com/r/tu-usuario/task-manager`
- **Repositorio**: `https://github.com/tu-usuario/task_manager_final`

---

## **🛠️ TROUBLESHOOTING RÁPIDO**

### **❌ Error: "Authentication failed"**
**Solución:** Verificar secretos DOCKER_USERNAME y DOCKER_PASSWORD en GitHub

### **❌ Error: "Tests failed"**
**Solución:** Revisar logs en GitHub Actions → Corregir errores → Nuevo commit

### **❌ Error: "Docker build failed"**
**Solución:** Verificar Dockerfile y dependencias → Probar build local

### **❌ Error: "Push failed"**
**Solución:** Verificar permisos del repositorio → Verificar configuración Git

---

## **📞 SOPORTE**

### **Documentación Adicional:**
- `README.md` - Documentación completa
- `DEPLOYMENT_INSTRUCTIONS.md` - Instrucciones detalladas
- `PROCEDIMIENTO_COMPLETO.md` - Procedimiento técnico completo

### **Comandos Útiles:**
```bash
# Ver estado del pipeline
git log --oneline -5

# Probar aplicación localmente
cd task_manager && python run.py

# Probar Docker localmente
docker build -t test . && docker run -p 5000:5000 test
```

**¡Tu pipeline CI/CD está completamente operativo!** 🚀 