from flask import request, jsonify

from services import nosql_services as svc
from utils.error_utils import explicar_error


def nosql_etiqueta():
    valor = request.args.get("valor", "")
    try:
        rows = svc.buscar_por_etiqueta(valor)
        return jsonify(
            _sql=svc.SQL_ETIQUETA.strip(), _params=[valor],
            _explica='Tabla afectada: PRODUCTO (columna JSONB datos_extra). Busca en el arreglo "etiquetas".',
            data=rows,
        )
    except Exception as e:
        return jsonify(_sql=svc.SQL_ETIQUETA.strip(), error=explicar_error(e)), 400


def nosql_alergeno():
    valor = request.args.get("valor", "")
    try:
        rows = svc.buscar_por_alergeno(valor)
        return jsonify(
            _sql=svc.SQL_ALERGENO.strip(), _params=[valor],
            _explica='Busca dentro del arreglo JSON "alergenos" de la tabla PRODUCTO.',
            data=rows,
        )
    except Exception as e:
        return jsonify(_sql=svc.SQL_ALERGENO.strip(), error=explicar_error(e)), 400
