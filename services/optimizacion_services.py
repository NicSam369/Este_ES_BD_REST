from database import get_conn, consultar
from services.reporte_services import SQL_VENTAS_POR_SUCURSAL

SQL_INDICES = """SELECT indexname, tablename, indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname"""


def explain_reporte_ventas():
    sql = "EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)\n" + SQL_VENTAS_POR_SUCURSAL.replace("%s", "0")
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            plan = "\n".join(r[0] for r in cur.fetchall())
        return sql, plan
    finally:
        conn.close()


def listar_indices():
    return SQL_INDICES, consultar(SQL_INDICES)
