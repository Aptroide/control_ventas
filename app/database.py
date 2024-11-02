import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

# Configuración de la conexión a la base de datos PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host= settings.DATABASE_URL,
            database= settings.DATABASE_NAME,
            user= settings.DATABASE_USER,
            password= settings.DATABASE_PASSWORD,
            cursor_factory=RealDictCursor
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error: {e}")

def execute_query(query, params=None, fetch="one"):
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        # Elige el método de fetch según el parámetro 'fetch'
        if fetch == "one":
            result = cursor.fetchone()
        elif fetch == "all":
            result = cursor.fetchall()
        else:
            result = None  # Para casos en los que no se espera un resultado (e.g., solo commit)
        
        conn.commit()
        return result
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        return e
        # raise e
    finally:
        cursor.close()
        conn.close()