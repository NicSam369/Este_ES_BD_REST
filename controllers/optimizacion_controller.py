from flask import jsonify

from services import optimizacion_services as svc
from services.reporte_services import SQL_VENTAS_POR_SUCURSAL
from utils.error_utils import explicar_error


def optimizacion_explain():
    sql_preview = "EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)\n" + SQL_VENTAS_POR_SUCURSAL.replace("%s", "0")
    try:
        sql, plan = svc.explain_reporte_ventas()
        return jsonify(_sql=sql.strip(), data=plan)
    except Exception as e:
        return jsonify(_sql=sql_preview.strip(), error=explicar_error(e)), 500


def optimizacion_indices():
    sql, data = svc.listar_indices()
    return jsonify(_sql=sql.strip(), data=data)
