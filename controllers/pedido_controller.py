from flask import request, jsonify

from services import pedido_services as svc


def listar_pedidos():
    sql, data = svc.listar_pedidos()
    return jsonify(_sql=sql.strip(), data=data)


def crear_pedido():
    b = request.get_json(silent=True) or {}
    try:
        pasos_sql, data = svc.crear_pedido(b)
        return jsonify(_sql=pasos_sql, data=data), 201
    except svc.PedidoError as e:
        return jsonify(_sql=e.sql_pasos, error=e.mensaje), 400
    except ValueError as e:
        # Validaciones previas a abrir transaccion (sin BEGIN todavia)
        return jsonify(error=str(e)), 400
