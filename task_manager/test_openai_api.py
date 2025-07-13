#!/usr/bin/env python3
"""
Script de prueba para la nueva API de OpenAI
"""

import os
from dotenv import load_dotenv
import openai

# Cargar variables de entorno
load_dotenv()

def test_openai_api():
    """Prueba la nueva API de OpenAI"""
    print("🧪 Probando nueva API de OpenAI...")
    
    try:
        # Configurar OpenAI para Azure (nueva API v1.x)
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        
        print(f"📋 API Key: {api_key[:10]}..." if api_key else "❌ No API Key")
        print(f"📋 API Version: {api_version}")
        print(f"📋 Azure Endpoint: {azure_endpoint}")
        print(f"📋 Deployment: {deployment_name}")
        
        if not all([api_key, api_version, azure_endpoint, deployment_name]):
            print("❌ Faltan variables de entorno")
            return False
        
        # Configurar OpenAI para Azure (nueva API v1.x)
        openai.api_key = api_key
        openai.api_version = api_version
        openai.azure_endpoint = azure_endpoint
        
        print("🔄 Configuración completada")
        
        # Probar llamada simple
        print("🔄 Probando llamada a la API...")
        response = openai.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "Eres un asistente útil."},
                {"role": "user", "content": "Di 'Hola mundo'"}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        print(f"✅ Respuesta recibida: {content}")
        print(f"📊 Tokens usados: {response.usage.total_tokens}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(f"   Tipo de error: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = test_openai_api()
    if success:
        print("\n🎉 ¡API de OpenAI funciona correctamente!")
    else:
        print("\n❌ Error en la API de OpenAI") 