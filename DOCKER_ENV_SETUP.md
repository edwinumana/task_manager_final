# 🐳 Configuración de Variables de Entorno para Docker

## 📋 Variables Requeridas

Para que la aplicación funcione correctamente en Docker, necesitas configurar las siguientes variables de entorno:

### 🔗 Azure MySQL
```bash
AZURE_MYSQL_CONNECTION_STRING=mysql://username:password@server:3306/database
AZURE_MYSQL_SSL_CA=/path/to/ca.pem
AZURE_MYSQL_SSL_VERIFY=true
```

### 🤖 Azure OpenAI
```bash
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2023-12-01-preview
```

### ⚙️ Configuración del Modelo
```bash
TEMPERATURE=0.7
MAX_TOKENS=1000
TOP_P=0.2
FREQUENCY_PENALTY=0.0
PRESENCE_PENALTY=0.0
```

## 🚀 Configuración en GitHub Actions

Las variables se configuran en **GitHub Repository Secrets**:

1. Ve a tu repositorio en GitHub
2. Settings → Secrets and variables → Actions
3. Añade cada variable como un **Repository Secret**

## 🛠️ Construcción Local con Docker

Si quieres construir la imagen localmente:

```bash
docker build \
  --build-arg AZURE_MYSQL_CONNECTION_STRING="your-connection-string" \
  --build-arg AZURE_OPENAI_API_KEY="your-api-key" \
  --build-arg AZURE_OPENAI_ENDPOINT="your-endpoint" \
  --build-arg AZURE_OPENAI_DEPLOYMENT_NAME="your-deployment" \
  --build-arg AZURE_OPENAI_API_VERSION="2023-12-01-preview" \
  --build-arg TEMPERATURE="0.7" \
  --build-arg MAX_TOKENS="1000" \
  --build-arg TOP_P="0.2" \
  --build-arg FREQUENCY_PENALTY="0.0" \
  --build-arg PRESENCE_PENALTY="0.0" \
  -t task-manager .
```

## 🏃 Ejecución Local con Docker

```bash
docker run -p 5000:5000 \
  -e AZURE_MYSQL_CONNECTION_STRING="your-connection-string" \
  -e AZURE_OPENAI_API_KEY="your-api-key" \
  -e AZURE_OPENAI_ENDPOINT="your-endpoint" \
  -e AZURE_OPENAI_DEPLOYMENT_NAME="your-deployment" \
  -e AZURE_OPENAI_API_VERSION="2023-12-01-preview" \
  -e TEMPERATURE="0.7" \
  -e MAX_TOKENS="1000" \
  -e TOP_P="0.2" \
  -e FREQUENCY_PENALTY="0.0" \
  -e PRESENCE_PENALTY="0.0" \
  task-manager
```

## 🔧 Solución de Problemas

### Error: "Variables de entorno no encontradas"
- Verifica que todas las variables estén configuradas en GitHub Secrets
- Asegúrate de que los nombres coincidan exactamente
- Revisa que no haya espacios extra en los valores

### Error: "Conexión a Azure MySQL falla"
- Verifica que la cadena de conexión sea correcta
- Asegúrate de que el certificado SSL esté configurado
- Comprueba que la base de datos esté accesible desde GitHub Actions

### Error: "Azure OpenAI no responde"
- Verifica que la API key sea válida
- Asegúrate de que el endpoint sea correcto
- Comprueba que el deployment name exista

## 📚 Referencias

- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Docker Build Args](https://docs.docker.com/engine/reference/builder/#arg)
- [Azure OpenAI Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/openai/) 