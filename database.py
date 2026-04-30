import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    db_url = os.environ.get("DATABASE_URL")
    try:
        if db_url:
            return psycopg2.connect(db_url)
        else:
            return psycopg2.connect(
                host="localhost",
                database="buscar_clima",
                user="postgres",
                password="1234",
                port="5432"
            )
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return None

def buscar_historico_clima(cidade, data):
    conn = get_connection()
    if not conn: return None
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        sql = 'SELECT * FROM public.historico_clima WHERE LOWER(cidade) = LOWER(%s) AND data = %s'
        cursor.execute(sql, (cidade, data))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro na busca: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def salvar_historico_clima(weather_data):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO public.historico_clima 
            (cidade, data, umidade, vento, precipitacao, temp_min, temp_max)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            weather_data['cidade'],
            weather_data['data'],
            weather_data['umidade'],
            weather_data['vento'],
            weather_data['precipitacao'],
            weather_data['temp_min'],
            weather_data['temp_max']
        )
        cursor.execute(sql, params)
        conn.commit()
        print(f"Dados de {weather_data['cidade']} salvos!")
        return True
    except Exception as e:
        print(f"Erro ao salvar: {e}")
        return False
    finally:
        cursor.close()
        conn.close()