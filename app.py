# =====================================================================
#  RESTAURANTE - API (Flask + PostgreSQL)
#  ADAPTADO al esquema de la miss (tablas PRODUCTO, PEDIDO, CLIENTE, etc.)
#
#  Cada endpoint devuelve el SQL que ejecuto (campo "_sql") para que en
#  la demo se vea exactamente que consulta corrio (Consola SQL del panel).
#
#  MAPA RUBRICA -> ENDPOINT:
#    * CRUD simple + constraints     -> /api/productos  (PRODUCTO)
#    * CRUD complejo 3+ tablas + TX  -> POST /api/pedidos (PEDIDO+DETALLE_PEDIDO+PRODUCTO)
#    * Reporte GROUP BY/HAVING+export-> /api/reportes/ventas-por-sucursal
#    * NoSQL / JSONB                 -> /api/nosql/*  (PRODUCTO.datos_extra)
#    * Optimizacion / EXPLAIN        -> /api/optimizacion/*
#
#  Este archivo SOLO crea la app de Flask y registra los Blueprints.
#  Toda la logica vive en routes/ -> controllers/ -> services/.
# =====================================================================
from flask import Flask, send_from_directory

from config import PORT
from routes.catalogo_routes import catalogo_bp
from routes.producto_routes import producto_bp
from routes.pedido_routes import pedido_bp
from routes.reporte_routes import reporte_bp
from routes.nosql_routes import nosql_bp
from routes.optimizacion_routes import optimizacion_bp

app = Flask(__name__, static_folder="public", static_url_path="")

app.register_blueprint(catalogo_bp)
app.register_blueprint(producto_bp)
app.register_blueprint(pedido_bp)
app.register_blueprint(reporte_bp)
app.register_blueprint(nosql_bp)
app.register_blueprint(optimizacion_bp)


@app.route("/")
def index():
    return send_from_directory("public", "index.html")


if __name__ == "__main__":
    print(f"\n  Restaurante API + Web (Python/Flask) en  http://localhost:{PORT}\n")
    app.run(host="0.0.0.0", port=PORT, debug=False)
