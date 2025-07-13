# 🔐 CONFIGURAR SECRETOS DOCKER HUB

## 📋 Paso a Paso para Configurar Secretos

### **PARTE A: Obtener Credenciales de Docker Hub**

#### **1. Crear/Verificar Cuenta Docker Hub**
1. Ir a [Docker Hub](https://hub.docker.com/)
2. Crear cuenta o iniciar sesión
3. **IMPORTANTE**: Anota tu nombre de usuario exacto

#### **2. Generar Access Token**
1. Hacer clic en tu **nombre de usuario** (esquina superior derecha)
2. Seleccionar **"Account Settings"**
3. Ir a la pestaña **"Security"**
4. Hacer clic en **"New Access Token"**
5. Configurar:
   ```
   Token Description: GitHub Actions CI/CD
   Permissions: ✅ Read, Write, Delete
   ```
6. Hacer clic en **"Generate"**
7. **⚠️ CRÍTICO**: Copiar el token INMEDIATAMENTE (no se mostrará de nuevo)

### **PARTE B: Configurar Secretos en GitHub**

#### **1. Ir a Configuración del Repositorio**
1. En tu repositorio `task_manager_final`
2. Hacer clic en **"Settings"** (pestaña del repositorio)
3. En el menú lateral izquierdo, buscar **"Secrets and variables"**
4. Hacer clic en **"Actions"**

#### **2. Agregar Primer Secreto**
1. Hacer clic en **"New repository secret"**
2. Configurar:
   ```
   Name: DOCKER_USERNAME
   Secret: tu-nombre-usuario-docker-hub
   ```
3. Hacer clic en **"Add secret"**

#### **3. Agregar Segundo Secreto**
1. Hacer clic en **"New repository secret"** otra vez
2. Configurar:
   ```
   Name: DOCKER_PASSWORD
   Secret: el-access-token-generado-en-paso-A2
   ```
3. Hacer clic en **"Add secret"**

### **✅ Verificación**
Deberías ver en la página de secretos:
- ✅ `DOCKER_USERNAME` - Updated X seconds ago
- ✅ `DOCKER_PASSWORD` - Updated X seconds ago

### **🧪 Prueba Local (Opcional)**
```bash
# Probar credenciales localmente
docker login
Username: tu-nombre-usuario
Password: el-access-token (NO tu password normal)
```

**¡Secretos configurados exitosamente!** 🔐 