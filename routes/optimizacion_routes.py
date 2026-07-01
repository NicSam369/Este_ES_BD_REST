from flask import Blueprint

from controllers import optimizacion_controller as ctrl

optimizacion_bp = Blueprint("optimizacion", __name__, url_prefix="/api/optimizacion")

optimizacion_bp.add_url_rule("/explain", view_func=ctrl.optimizacion_explain, methods=["GET"])
optimizacion_bp.add_url_rule("/indices", view_func=ctrl.optimizacion_indices, methods=["GET"])
