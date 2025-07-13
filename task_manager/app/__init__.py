from flask import Flask, redirect
from config import Config
from flask_cors import CORS
from app.routes.ai_routes import ai_bp
from app.database.migrations import init_database, test_database_connection
from app.routes.user_story_routes import user_story_routes

def create_app(config_class=Config):
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__, 
                template_folder='templates',  # Carpeta donde están las plantillas
                static_folder='static')       # Carpeta para archivos estáticos
    
    # Configuración
    app.config.from_object(config_class)
    
    # Inicializar base de datos Azure MySQL
    with app.app_context():
        try:
            print("🔍 Probando conexión a Azure MySQL...")
            if test_database_connection():
                print("✅ Conexión a Azure MySQL exitosa")
                print("🚀 Inicializando base de datos...")
                if init_database():
                    print("✅ Base de datos inicializada exitosamente")
                else:
                    print("⚠️ Error al inicializar base de datos")
            else:
                print("⚠️ No se pudo conectar a Azure MySQL - usando modo JSON")
        except Exception as e:
            print(f"⚠️ Error en configuración de base de datos: {str(e)}")
    
    # Registrar blueprints
    from app.routes.task_routes import task_bp
    app.register_blueprint(task_bp, url_prefix='/tasks')
    app.register_blueprint(ai_bp, url_prefix='/ai')
    app.register_blueprint(user_story_routes)
    
    # Redirigir la raíz a /tasks
    @app.route('/')
    def root():
        return redirect('/tasks')
    
    return app