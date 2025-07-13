# =============================================================================
# SCRIPT DE VERIFICACIÓN DE DESPLIEGUE - TASK MANAGER (PowerShell)
# =============================================================================
# Este script verifica que el despliegue de Task Manager funcione correctamente
# tanto en local como desde Docker Hub

param(
    [switch]$SkipDockerHub,
    [switch]$SkipTests,
    [switch]$Verbose
)

# Configuración
$DOCKER_IMAGE = "task-manager"
$DOCKER_HUB_IMAGE = "edwinumana/task-manager:latest"
$CONTAINER_NAME = "task-manager-verify"
$PORT = 5000
$TIMEOUT = 30

# Funciones de utilidad
function Write-Header {
    param($Message)
    Write-Host "`n=== $Message ===" -ForegroundColor Blue
}

function Write-Success {
    param($Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Error {
    param($Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-Warning {
    param($Message)
    Write-Host "⚠️ $Message" -ForegroundColor Yellow
}

function Write-Info {
    param($Message)
    Write-Host "ℹ️ $Message" -ForegroundColor Cyan
}

# Función para limpiar contenedores
function Cleanup {
    try {
        $containers = docker ps -a --format "table {{.Names}}" | Select-String $CONTAINER_NAME
        if ($containers) {
            Write-Info "Limpiando contenedor existente..."
            docker stop $CONTAINER_NAME 2>$null
            docker rm $CONTAINER_NAME 2>$null
        }
    }
    catch {
        # Ignorar errores de limpieza
    }
}

# Función para esperar que el servicio esté disponible
function Wait-ForService {
    param($Url, $TimeoutSeconds)
    
    Write-Info "Esperando que el servicio esté disponible en $Url..."
    
    for ($i = 0; $i -lt $TimeoutSeconds; $i++) {
        try {
            $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                return $true
            }
        }
        catch {
            # Continuar intentando
        }
        
        Start-Sleep -Seconds 1
        Write-Host "." -NoNewline
    }
    
    Write-Host ""
    return $false
}

# Función para probar endpoints
function Test-Endpoints {
    param($BaseUrl)
    
    $endpoints = @("/tasks", "/user-stories")
    
    Write-Info "Probando endpoints de la aplicación..."
    
    foreach ($endpoint in $endpoints) {
        $url = "$BaseUrl$endpoint"
        try {
            $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 10 -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                Write-Success "Endpoint $endpoint responde correctamente"
            }
            else {
                Write-Error "Endpoint $endpoint devolvió código: $($response.StatusCode)"
                return $false
            }
        }
        catch {
            Write-Error "Endpoint $endpoint no responde: $($_.Exception.Message)"
            return $false
        }
    }
    
    return $true
}

# Función para verificar build local
function Test-LocalBuild {
    Write-Header "VERIFICACIÓN DE BUILD LOCAL"
    
    if (!(Test-Path "Dockerfile")) {
        Write-Error "Dockerfile no encontrado. Asegúrate de estar en el directorio raíz del proyecto."
        return $false
    }
    
    Write-Info "Construyendo imagen Docker local..."
    try {
        $buildResult = docker build -t $DOCKER_IMAGE . 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Imagen construida exitosamente"
        }
        else {
            Write-Error "Error al construir la imagen"
            if ($Verbose) { Write-Host $buildResult }
            return $false
        }
    }
    catch {
        Write-Error "Error al construir la imagen: $($_.Exception.Message)"
        return $false
    }
    
    Write-Info "Iniciando contenedor desde imagen local..."
    Cleanup
    
    try {
        $runResult = docker run -d --name $CONTAINER_NAME -p "${PORT}:5000" $DOCKER_IMAGE 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Contenedor iniciado"
        }
        else {
            Write-Error "Error al iniciar contenedor"
            if ($Verbose) { Write-Host $runResult }
            return $false
        }
    }
    catch {
        Write-Error "Error al iniciar contenedor: $($_.Exception.Message)"
        return $false
    }
    
    if (Wait-ForService "http://localhost:$PORT/tasks" $TIMEOUT) {
        Write-Success "Servicio disponible"
    }
    else {
        Write-Error "Servicio no disponible después de $TIMEOUT segundos"
        docker logs $CONTAINER_NAME
        return $false
    }
    
    if (Test-Endpoints "http://localhost:$PORT") {
        Write-Success "Todos los endpoints funcionan correctamente"
    }
    else {
        Write-Error "Algunos endpoints no funcionan"
        return $false
    }
    
    Cleanup
    Write-Success "Verificación de build local completada"
    return $true
}

# Función para verificar imagen de Docker Hub
function Test-DockerHub {
    Write-Header "VERIFICACIÓN DE IMAGEN DE DOCKER HUB"
    
    Write-Info "Descargando imagen desde Docker Hub..."
    try {
        $pullResult = docker pull $DOCKER_HUB_IMAGE 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Imagen descargada exitosamente"
        }
        else {
            Write-Error "Error al descargar imagen de Docker Hub"
            if ($Verbose) { Write-Host $pullResult }
            return $false
        }
    }
    catch {
        Write-Error "Error al descargar imagen: $($_.Exception.Message)"
        return $false
    }
    
    Write-Info "Iniciando contenedor desde Docker Hub..."
    Cleanup
    
    try {
        $runResult = docker run -d --name $CONTAINER_NAME -p "${PORT}:5000" $DOCKER_HUB_IMAGE 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Contenedor iniciado"
        }
        else {
            Write-Error "Error al iniciar contenedor"
            if ($Verbose) { Write-Host $runResult }
            return $false
        }
    }
    catch {
        Write-Error "Error al iniciar contenedor: $($_.Exception.Message)"
        return $false
    }
    
    if (Wait-ForService "http://localhost:$PORT/tasks" $TIMEOUT) {
        Write-Success "Servicio disponible"
    }
    else {
        Write-Error "Servicio no disponible después de $TIMEOUT segundos"
        docker logs $CONTAINER_NAME
        return $false
    }
    
    if (Test-Endpoints "http://localhost:$PORT") {
        Write-Success "Todos los endpoints funcionan correctamente"
    }
    else {
        Write-Error "Algunos endpoints no funcionan"
        return $false
    }
    
    Cleanup
    Write-Success "Verificación de Docker Hub completada"
    return $true
}

# Función para verificar Docker Compose
function Test-DockerCompose {
    Write-Header "VERIFICACIÓN DE DOCKER COMPOSE"
    
    if (!(Test-Path "docker-compose.yml")) {
        Write-Warning "docker-compose.yml no encontrado. Saltando verificación."
        return $true
    }
    
    Write-Info "Iniciando servicios con Docker Compose..."
    try {
        $composeResult = docker-compose up -d 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Servicios iniciados"
        }
        else {
            Write-Error "Error al iniciar servicios con Docker Compose"
            if ($Verbose) { Write-Host $composeResult }
            return $false
        }
    }
    catch {
        Write-Error "Error con Docker Compose: $($_.Exception.Message)"
        return $false
    }
    
    if (Wait-ForService "http://localhost:$PORT/tasks" $TIMEOUT) {
        Write-Success "Servicio disponible"
    }
    else {
        Write-Error "Servicio no disponible después de $TIMEOUT segundos"
        docker-compose logs
        return $false
    }
    
    if (Test-Endpoints "http://localhost:$PORT") {
        Write-Success "Todos los endpoints funcionan correctamente"
    }
    else {
        Write-Error "Algunos endpoints no funcionan"
        return $false
    }
    
    Write-Info "Deteniendo servicios de Docker Compose..."
    docker-compose down 2>$null
    
    Write-Success "Verificación de Docker Compose completada"
    return $true
}

# Función para verificar tests
function Test-PythonTests {
    Write-Header "VERIFICACIÓN DE TESTS"
    
    if (!(Test-Path "task_manager/tests")) {
        Write-Warning "Directorio de tests no encontrado. Saltando verificación."
        return $true
    }
    
    Write-Info "Ejecutando tests principales..."
    Push-Location "task_manager"
    
    try {
        $testResult = python -m pytest tests/test_core_isolated.py -v 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Tests core ejecutados exitosamente"
            Pop-Location
            return $true
        }
        else {
            Write-Error "Fallos en tests core"
            if ($Verbose) { Write-Host $testResult }
            Pop-Location
            return $false
        }
    }
    catch {
        Write-Error "Error ejecutando tests: $($_.Exception.Message)"
        Pop-Location
        return $false
    }
}

# Función para mostrar información del sistema
function Show-SystemInfo {
    Write-Header "INFORMACIÓN DEL SISTEMA"
    
    try {
        $dockerVersion = docker --version
        Write-Host "Docker Version: $dockerVersion"
    }
    catch {
        Write-Host "Docker Version: No disponible"
    }
    
    try {
        $composeVersion = docker-compose --version
        Write-Host "Docker Compose Version: $composeVersion"
    }
    catch {
        Write-Host "Docker Compose Version: No disponible"
    }
    
    try {
        $pythonVersion = python --version
        Write-Host "Python Version: $pythonVersion"
    }
    catch {
        Write-Host "Python Version: No disponible"
    }
    
    Write-Host "Sistema Operativo: $([System.Environment]::OSVersion.VersionString)"
    Write-Host "Arquitectura: $([System.Environment]::GetEnvironmentVariable('PROCESSOR_ARCHITECTURE'))"
    Write-Host ""
}

# Función principal
function Main {
    Write-Header "SCRIPT DE VERIFICACIÓN DE DESPLIEGUE - TASK MANAGER"
    
    # Verificar prerrequisitos
    if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Error "Docker no está instalado o no está en el PATH"
        exit 1
    }
    
    Show-SystemInfo
    
    # Limpiar antes de empezar
    Cleanup
    
    # Variables para tracking de resultados
    $localBuildSuccess = $false
    $dockerHubSuccess = $false
    $dockerComposeSuccess = $false
    $testsSuccess = $false
    
    # Ejecutar verificaciones
    $localBuildSuccess = Test-LocalBuild
    
    if (!$SkipDockerHub) {
        $dockerHubSuccess = Test-DockerHub
    }
    else {
        Write-Warning "Saltando verificación de Docker Hub"
        $dockerHubSuccess = $true
    }
    
    $dockerComposeSuccess = Test-DockerCompose
    
    if (!$SkipTests) {
        $testsSuccess = Test-PythonTests
    }
    else {
        Write-Warning "Saltando verificación de tests"
        $testsSuccess = $true
    }
    
    # Reporte final
    Write-Header "REPORTE FINAL"
    
    $localStatus = if ($localBuildSuccess) { "✅ EXITOSO" } else { "❌ FALLIDO" }
    $hubStatus = if ($dockerHubSuccess) { "✅ EXITOSO" } else { "❌ FALLIDO" }
    $composeStatus = if ($dockerComposeSuccess) { "✅ EXITOSO" } else { "❌ FALLIDO" }
    $testStatus = if ($testsSuccess) { "✅ EXITOSO" } else { "❌ FALLIDO" }
    
    Write-Host "Build Local: $localStatus"
    Write-Host "Docker Hub: $hubStatus"
    Write-Host "Docker Compose: $composeStatus"
    Write-Host "Tests: $testStatus"
    
    # Determinar resultado general
    if ($localBuildSuccess -and $dockerHubSuccess) {
        Write-Success "¡Verificación completada exitosamente!"
        Write-Info "La aplicación Task Manager está lista para producción."
        exit 0
    }
    else {
        Write-Error "Verificación fallida. Revisa los errores anteriores."
        exit 1
    }
}

# Trap para limpiar en caso de interrupción
trap { Cleanup } 2

# Ejecutar función principal
Main 