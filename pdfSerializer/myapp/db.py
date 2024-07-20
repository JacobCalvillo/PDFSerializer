from dotenv import load_dotenv
import os
import psycopg2 

# Carga las variables de entorno desde .env
load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'))
        return conn
    except psycopg2.DatabaseError as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise e