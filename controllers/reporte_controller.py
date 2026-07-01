from flask import request, jsonify, Response

from services import reporte_services as svc
from utils.error_utils import explicar_error


def reporte_ventas():
    try:
        minimo = float(request.args.get("min", 0))
    except ValueError:
        minimo = 0
    formato = (request.args.get("formato", "json") or "json").lower()

    try:
        rows = svc.ventas_por_sucursal(minimo)
    except Exception as e:
        return jsonify(_sql=svc.SQL_VENTAS_POR_SUCURSAL.strip(), error=explicar_error(e)), 500

    if formato == "json":
        return jsonify(_sql=svc.SQL_VENTAS_POR_SUCURSAL.strip(), _params=[minimo], data=rows)

    if formato == "csv":
        contenido = svc.exportar_csv(rows)
        return Response(
            contenido,
            mimetype="text/csv; charset=utf-8",
            headers={"Content-Disposition": 'attachment; filename="ventas_por_sucursal.csv"'},
        )

    if formato == "excel":
        contenido = svc.exportar_excel(rows)
        return Response(
            contenido,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": 'attachment; filename="ventas_por_sucursal.xlsx"'},
        )

    return jsonify(error="Formato no soportado. Use json, csv o excel."), 400


def reporte_productos():
    sql, data = svc.productos_mas_vendidos()
    return jsonify(_sql=sql.strip(), data=data)
