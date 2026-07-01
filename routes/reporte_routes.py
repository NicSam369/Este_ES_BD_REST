from flask import Blueprint

from controllers import reporte_controller as ctrl

reporte_bp = Blueprint("reporte", __name__, url_prefix="/api/reportes")

reporte_bp.add_url_rule("/ventas-por-sucursal", view_func=ctrl.reporte_ventas, methods=["GET"])
reporte_bp.add_url_rule("/productos-mas-vendidos", view_func=ctrl.reporte_productos, methods=["GET"])
