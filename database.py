import psycopg2
import psycopg2.extras

from config import DATABASE_URL


def get_conn():
    """Abre una conexion nueva a PostgreSQL."""
    return psycopg2.connect(DATABASE_URL)


def consultar(sql, params=None):
    """Ejecuta un SELECT y devuelve las filas como lista de dicts."""
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params or [])
            return cur.fetchall()
    finally:
        conn.close()
