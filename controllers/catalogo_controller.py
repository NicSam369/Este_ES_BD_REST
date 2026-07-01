from flask import jsonify

from services import catalogo_services as svc


def categorias():
    sql, data = svc.listar_categorias()
    return jsonify(_sql=sql, data=data)


def clientes():
    sql, data = svc.listar_clientes()
    return jsonify(_sql=sql, data=data)


def mesas():
    sql, data = svc.listar_mesas()
    return jsonify(_sql=sql, data=data)


def empleados():
    sql, data = svc.listar_empleados()
    return jsonify(_sql=sql, data=data)
