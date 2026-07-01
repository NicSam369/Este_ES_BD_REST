from flask import Blueprint

from controllers import catalogo_controller as ctrl

catalogo_bp = Blueprint("catalogo", __name__, url_prefix="/api")

catalogo_bp.add_url_rule("/categorias", view_func=ctrl.categorias, methods=["GET"])
catalogo_bp.add_url_rule("/clientes", view_func=ctrl.clientes, methods=["GET"])
catalogo_bp.add_url_rule("/mesas", view_func=ctrl.mesas, methods=["GET"])
catalogo_bp.add_url_rule("/empleados", view_func=ctrl.empleados, methods=["GET"])
