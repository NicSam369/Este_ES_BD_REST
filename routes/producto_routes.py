from flask import Blueprint

from controllers import producto_controller as ctrl

producto_bp = Blueprint("producto", __name__, url_prefix="/api/productos")

producto_bp.add_url_rule("", view_func=ctrl.listar_productos, methods=["GET"])
producto_bp.add_url_rule("", view_func=ctrl.crear_producto, methods=["POST"])
producto_bp.add_url_rule("/<int:pid>", view_func=ctrl.editar_producto, methods=["PUT"])
producto_bp.add_url_rule("/<int:pid>", view_func=ctrl.borrar_producto, methods=["DELETE"])
