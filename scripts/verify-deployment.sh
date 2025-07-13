#!/bin/bash

# =============================================================================
# SCRIPT DE VERIFICACIÓN DE DESPLIEGUE - TASK MANAGER
# =============================================================================
# Este script verifica que el despliegue de Task Manager funcione correctamente
# tanto en local como desde Docker Hub

set -e  # Salir en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
DOCKER_IMAGE="task-manager"
DOCKER_HUB_IMAGE="edwinumana/task-manager:latest"
CONTAINER_NAME="task-manager-verify"
PORT=5000
TIMEOUT=30

# Funciones de utilidad
print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

# Función para limpiar contenedores
cleanup() {
    if docker ps -a --format "table {{.Names}}" | grep -q "$CONTAINER_NAME"; then
        print_info "Limpiando contenedor existente..."
        docker stop "$CONTAINER_NAME" 2>/dev/null || true
        docker rm "$CONTAINER_NAME" 2>/dev/null || true
    fi
}

# Función para esperar que el servicio esté disponible
wait_for_service() {
    local url=$1
    local timeout=$2
    local counter=0
    
    print_info "Esperando que el servicio esté disponible en $url..."
    
    while [ $counter -lt $timeout ]; do
        if curl -f -s "$url" > /dev/null 2>&1; then
            return 0
        fi
        sleep 1
        ((counter++))
        printf "."
    done
    
    echo ""
    return 1
}

# Función para probar endpoints
test_endpoints() {
    local base_url=$1
    local endpoints=("/tasks" "/user-stories")
    
    print_info "Probando endpoints de la aplicación..."
    
    for endpoint in "${endpoints[@]}"; do
        local url="$base_url$endpoint"
        if curl -f -s "$url" > /dev/null 2>&1; then
            print_success "Endpoint $endpoint responde correctamente"
        else
            print_error "Endpoint $endpoint no responde"
            return 1
        fi
    done
    
    return 0
}

# Función para verificar build local
verify_local_build() {
    print_header "VERIFICACIÓN DE BUILD LOCAL"
    
    if [ ! -f "Dockerfile" ]; then
        print_error "Dockerfile no encontrado. Asegúrate de estar en el directorio raíz del proyecto."
        return 1
    fi
    
    print_info "Construyendo imagen Docker local..."
    if docker build -t "$DOCKER_IMAGE" . > /dev/null 2>&1; then
        print_success "Imagen construida exitosamente"
    else
        print_error "Error al construir la imagen"
        return 1
    fi
    
    print_info "Iniciando contenedor desde imagen local..."
    cleanup
    
    if docker run -d --name "$CONTAINER_NAME" -p "$PORT:5000" "$DOCKER_IMAGE" > /dev/null 2>&1; then
        print_success "Contenedor iniciado"
    else
        print_error "Error al iniciar contenedor"
        return 1
    fi
    
    if wait_for_service "http://localhost:$PORT/tasks" $TIMEOUT; then
        print_success "Servicio disponible"
    else
        print_error "Servicio no disponible después de $TIMEOUT segundos"
        docker logs "$CONTAINER_NAME"
        return 1
    fi
    
    if test_endpoints "http://localhost:$PORT"; then
        print_success "Todos los endpoints funcionan correctamente"
    else
        print_error "Algunos endpoints no funcionan"
        return 1
    fi
    
    cleanup
    print_success "Verificación de build local completada"
    return 0
}

# Función para verificar imagen de Docker Hub
verify_docker_hub() {
    print_header "VERIFICACIÓN DE IMAGEN DE DOCKER HUB"
    
    print_info "Descargando imagen desde Docker Hub..."
    if docker pull "$DOCKER_HUB_IMAGE" > /dev/null 2>&1; then
        print_success "Imagen descargada exitosamente"
    else
        print_error "Error al descargar imagen de Docker Hub"
        return 1
    fi
    
    print_info "Iniciando contenedor desde Docker Hub..."
    cleanup
    
    if docker run -d --name "$CONTAINER_NAME" -p "$PORT:5000" "$DOCKER_HUB_IMAGE" > /dev/null 2>&1; then
        print_success "Contenedor iniciado"
    else
        print_error "Error al iniciar contenedor"
        return 1
    fi
    
    if wait_for_service "http://localhost:$PORT/tasks" $TIMEOUT; then
        print_success "Servicio disponible"
    else
        print_error "Servicio no disponible después de $TIMEOUT segundos"
        docker logs "$CONTAINER_NAME"
        return 1
    fi
    
    if test_endpoints "http://localhost:$PORT"; then
        print_success "Todos los endpoints funcionan correctamente"
    else
        print_error "Algunos endpoints no funcionan"
        return 1
    fi
    
    cleanup
    print_success "Verificación de Docker Hub completada"
    return 0
}

# Función para verificar Docker Compose
verify_docker_compose() {
    print_header "VERIFICACIÓN DE DOCKER COMPOSE"
    
    if [ ! -f "docker-compose.yml" ]; then
        print_warning "docker-compose.yml no encontrado. Saltando verificación."
        return 0
    fi
    
    print_info "Iniciando servicios con Docker Compose..."
    if docker-compose up -d > /dev/null 2>&1; then
        print_success "Servicios iniciados"
    else
        print_error "Error al iniciar servicios con Docker Compose"
        return 1
    fi
    
    if wait_for_service "http://localhost:$PORT/tasks" $TIMEOUT; then
        print_success "Servicio disponible"
    else
        print_error "Servicio no disponible después de $TIMEOUT segundos"
        docker-compose logs
        return 1
    fi
    
    if test_endpoints "http://localhost:$PORT"; then
        print_success "Todos los endpoints funcionan correctamente"
    else
        print_error "Algunos endpoints no funcionan"
        return 1
    fi
    
    print_info "Deteniendo servicios de Docker Compose..."
    docker-compose down > /dev/null 2>&1
    
    print_success "Verificación de Docker Compose completada"
    return 0
}

# Función para verificar tests
verify_tests() {
    print_header "VERIFICACIÓN DE TESTS"
    
    if [ ! -d "task_manager/tests" ]; then
        print_warning "Directorio de tests no encontrado. Saltando verificación."
        return 0
    fi
    
    print_info "Ejecutando tests principales..."
    cd task_manager
    
    if python -m pytest tests/test_core_isolated.py -v > /dev/null 2>&1; then
        print_success "Tests core ejecutados exitosamente"
    else
        print_error "Fallos en tests core"
        cd ..
        return 1
    fi
    
    cd ..
    print_success "Verificación de tests completada"
    return 0
}

# Función para mostrar información del sistema
show_system_info() {
    print_header "INFORMACIÓN DEL SISTEMA"
    
    echo "Docker Version: $(docker --version)"
    echo "Docker Compose Version: $(docker-compose --version 2>/dev/null || echo 'No disponible')"
    echo "Python Version: $(python --version 2>/dev/null || echo 'No disponible')"
    echo "Sistema Operativo: $(uname -s)"
    echo "Arquitectura: $(uname -m)"
    echo ""
}

# Función principal
main() {
    print_header "SCRIPT DE VERIFICACIÓN DE DESPLIEGUE - TASK MANAGER"
    
    # Verificar prerrequisitos
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado o no está en el PATH"
        exit 1
    fi
    
    if ! command -v curl &> /dev/null; then
        print_error "curl no está instalado o no está en el PATH"
        exit 1
    fi
    
    show_system_info
    
    # Limpiar antes de empezar
    cleanup
    
    # Variables para tracking de resultados
    local_build_success=false
    docker_hub_success=false
    docker_compose_success=false
    tests_success=false
    
    # Ejecutar verificaciones
    if verify_local_build; then
        local_build_success=true
    fi
    
    if verify_docker_hub; then
        docker_hub_success=true
    fi
    
    if verify_docker_compose; then
        docker_compose_success=true
    fi
    
    if verify_tests; then
        tests_success=true
    fi
    
    # Reporte final
    print_header "REPORTE FINAL"
    
    echo "Build Local: $([ "$local_build_success" = true ] && echo -e "${GREEN}✅ EXITOSO${NC}" || echo -e "${RED}❌ FALLIDO${NC}")"
    echo "Docker Hub: $([ "$docker_hub_success" = true ] && echo -e "${GREEN}✅ EXITOSO${NC}" || echo -e "${RED}❌ FALLIDO${NC}")"
    echo "Docker Compose: $([ "$docker_compose_success" = true ] && echo -e "${GREEN}✅ EXITOSO${NC}" || echo -e "${RED}❌ FALLIDO${NC}")"
    echo "Tests: $([ "$tests_success" = true ] && echo -e "${GREEN}✅ EXITOSO${NC}" || echo -e "${RED}❌ FALLIDO${NC}")"
    
    # Determinar resultado general
    if [ "$local_build_success" = true ] && [ "$docker_hub_success" = true ]; then
        print_success "¡Verificación completada exitosamente!"
        print_info "La aplicación Task Manager está lista para producción."
        exit 0
    else
        print_error "Verificación fallida. Revisa los errores anteriores."
        exit 1
    fi
}

# Trap para limpiar en caso de interrupción
trap cleanup EXIT

# Ejecutar función principal
main "$@" 