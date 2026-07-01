import io
import csv

from database import consultar, get_conn

SQL_VENTAS_POR_SUCURSAL = """SELECT s.nombre                  AS sucursal,
       COUNT(DISTINCT p.id_pedido)     AS total_pedidos,
       COALESCE(SUM(p.total), 0)       AS total_ventas
FROM SUCURSAL s
LEFT JOIN MESA   m ON s.id_scrsal = m.id_scrsal
LEFT JOIN PEDIDO p ON m.id_mesa   = p.id_mesa
GROUP BY s.id_scrsal, s.nombre
HAVING COALESCE(SUM(p.total), 0) > %s
ORDER BY total_ventas DESC"""

SQL_PRODUCTOS_MAS_VENDIDOS = """SELECT pr.nombre AS producto, SUM(dp.cantidad) AS unidades_vendidas
FROM PRODUCTO pr
JOIN DETALLE_PEDIDO dp ON pr.id_producto = dp.id_producto
GROUP BY pr.id_producto, pr.nombre
HAVING SUM(dp.cantidad) > 0
ORDER BY unidades_vendidas DESC"""


def ventas_por_sucursal(minimo):
    return consultar(SQL_VENTAS_POR_SUCURSAL, [minimo])


def productos_mas_vendidos():
    return SQL_PRODUCTOS_MAS_VENDIDOS, consultar(SQL_PRODUCTOS_MAS_VENDIDOS)


def exportar_csv(rows):
    cab = ["sucursal", "total_pedidos", "total_ventas"]
    buf = io.StringIO()
    buf.write("\ufeff")  # BOM para acentos en Excel
    w = csv.writer(buf)
    w.writerow(["Sucursal", "Total pedidos", "Total ventas"])
    for r in rows:
        w.writerow([r[k] for k in cab])
    return buf.getvalue()


def exportar_excel(rows):
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Ventas"
    ws.append(["Sucursal", "Total pedidos", "Total ventas"])
    for celda in ws[1]:
        celda.font = celda.font.copy(bold=True)
    for r in rows:
        ws.append([r["sucursal"], r["total_pedidos"], float(r["total_ventas"] or 0)])
    out = io.BytesIO()
    wb.save(out)
    out.seek(0)
    return out.getvalue()
