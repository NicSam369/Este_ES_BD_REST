from flask import request, jsonify

from services import producto_services as svc
from utils.error_utils import explicar_error


def listar_productos():
    sql, data = svc.listar_productos()
    try:
        return jsonify(_sql=sql.strip(), data=data)
    except Exception as e:
        return jsonify(_sql=sql.strip(), error=explicar_error(e)), 500


def crear_producto():
    b = request.get_json(silent=True) or {}
    try:
        sql, params, row = svc.crear_producto(b)
        return jsonify(_sql=sql.strip(), _params=params, data=row), 201
    except Exception as e:
        return jsonify(_sql=svc.SQL_CREAR.strip(), error=explicar_error(e)), 400


def editar_producto(pid):
    b = request.get_json(silent=True) or {}
    try:
        sql, params, row = svc.editar_producto(pid, b)
        if row is None:
            return jsonify(error="No existe el producto."), 404
        return jsonify(_sql=sql.strip(), _params=params, data=row)
    except Exception as e:
        return jsonify(_sql=svc.SQL_EDITAR.strip(), error=explicar_error(e)), 400


def borrar_producto(pid):
    try:
        sql, row = svc.borrar_producto(pid)
        if row is None:
            return jsonify(error="No existe el producto."), 404
        return jsonify(_sql=sql, _params=[pid], data=row)
    except Exception as e:
        return jsonify(_sql=svc.SQL_BORRAR, error=explicar_error(e)), 400
