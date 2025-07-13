from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

connection_string = os.getenv('AZURE_MYSQL_CONNECTION_STRING')
ssl_ca = os.getenv('AZURE_MYSQL_SSL_CA')
ssl_verify = os.getenv('AZURE_MYSQL_SSL_VERIFY', 'true').lower() == 'true'

ssl_config = {}
if ssl_ca:
    ssl_config = {
        'ssl': {
            'ca': ssl_ca,
            'verify_cert': ssl_verify
        }
    }

engine = create_engine(connection_string, connect_args=ssl_config)

with engine.connect() as conn:
    # Añadir la columna si no existe
    try:
        conn.execute(text('ALTER TABLE tasks ADD COLUMN user_story_id INT NULL;'))
        print('✅ Columna user_story_id añadida a tasks.')
    except Exception as e:
        print(f'⚠️ Error o la columna ya existe: {e}')
    # Añadir la clave foránea
    try:
        conn.execute(text('ALTER TABLE tasks ADD CONSTRAINT fk_user_story FOREIGN KEY (user_story_id) REFERENCES user_story(id);'))
        print('✅ Clave foránea añadida.')
    except Exception as e:
        print(f'⚠️ Error o la clave foránea ya existe: {e}') 