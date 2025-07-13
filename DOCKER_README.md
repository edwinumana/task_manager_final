# Task Manager - Contenedor Docker

Este documento explica cómo ejecutar la aplicación Task Manager usando Docker.

## Requisitos Previos

- Docker instalado en tu sistema
- Docker Compose (opcional, pero recomendado)

## Construcción del Contenedor

### Opción 1: Usando Docker directamente

```bash
# Construir la imagen
docker build -t task-manager .

# Ejecutar el contenedor
docker run -p 5000:5000 task-manager
```

### Opción 2: Usando Docker Compose (Recomendado)

```bash
# Construir y ejecutar
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d --build
```

## Configuración de Variables de Entorno

Si necesitas conectar a Azure MySQL, crea un archivo `.env` en el directorio raíz:

```env
SECRET_KEY=tu-clave-secreta-aqui
AZURE_MYSQL_CONNECTION_STRING=tu-string-de-conexion
AZURE_MYSQL_SSL_CA=/path/to/ca-cert.pem
AZURE_MYSQL_SSL_VERIFY=true
```

O configura las variables directamente en el comando docker:

```bash
docker run -p 5000:5000 \
  -e SECRET_KEY=tu-clave-secreta \
  -e AZURE_MYSQL_CONNECTION_STRING=tu-string-de-conexion \
  task-manager
```

## Acceso a la Aplicación

Una vez que el contenedor esté ejecutándose, puedes acceder a la aplicación en:

- **URL**: http://localhost:5000
- **Puerto**: 5000

## Comandos Útiles

```bash
# Ver contenedores en ejecución
docker ps

# Ver logs del contenedor
docker-compose logs -f

# Detener el contenedor
docker-compose down

# Reconstruir sin caché
docker-compose build --no-cache

# Ejecutar comandos dentro del contenedor
docker-compose exec task-manager /bin/bash
```

## Estructura del Dockerfile

El Dockerfile incluye:

- **Imagen base**: Python 3.9-slim
- **Dependencias del sistema**: gcc, libmysqlclient-dev (para MySQL)
- **Puerto expuesto**: 5000
- **Directorio de trabajo**: /app
- **Variables de entorno**: Optimizadas para Python

## Persistencia de Datos

El archivo `docker-compose.yml` incluye un volumen para persistir los datos:

```yaml
volumes:
  - ./task_manager/data:/app/data
```

Esto significa que los datos se guardarán en `./task_manager/data` en tu sistema local.

## Solución de Problemas

### Error de conexión a MySQL
Si la aplicación no puede conectarse a Azure MySQL, verificará automáticamente y usará el modo JSON como respaldo.

### Puerto ya en uso
Si el puerto 5000 está ocupado, puedes cambiarlo en el `docker-compose.yml`:

```yaml
ports:
  - "8080:5000"  # Usar puerto 8080 en lugar de 5000
```

### Problemas de permisos
En sistemas Linux/Mac, asegúrate de que el directorio `data` tenga los permisos correctos:

```bash
chmod 755 task_manager/data
``` 