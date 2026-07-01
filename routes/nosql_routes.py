from flask import Blueprint

from controllers import nosql_controller as ctrl

nosql_bp = Blueprint("nosql", __name__, url_prefix="/api/nosql")

nosql_bp.add_url_rule("/etiqueta", view_func=ctrl.nosql_etiqueta, methods=["GET"])
nosql_bp.add_url_rule("/alergeno", view_func=ctrl.nosql_alergeno, methods=["GET"])
