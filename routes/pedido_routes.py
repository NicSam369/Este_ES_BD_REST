from flask import Blueprint

from controllers import pedido_controller as ctrl

pedido_bp = Blueprint("pedido", __name__, url_prefix="/api/pedidos")

pedido_bp.add_url_rule("", view_func=ctrl.listar_pedidos, methods=["GET"])
pedido_bp.add_url_rule("", view_func=ctrl.crear_pedido, methods=["POST"])
