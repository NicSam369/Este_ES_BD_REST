import psycopg2.extras

from database import get_conn, consultar
from utils.error_utils import explicar_error


class PedidoError(Exception):
    """Envuelve un error de negocio o de BD, conservando el log de pasos SQL
    ejecutados hasta el momento del ROLLBACK (para mostrarlo en la demo)."""

    def __init__(self, mensaje, sql_pasos):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.sql_pasos = sql_pasos

SQL_LISTAR = """SELECT p.id_pedido AS id, p.fecha_hora, p.estado, p.total,
       cl.nombre || ' ' || cl.apellido AS cliente,
       m.numero AS mesa,
       e.nombre || ' ' || e.apellido AS mesero
FROM PEDIDO p
LEFT JOIN CLIENTE  cl ON cl.id_cliente  = p.id_cliente
LEFT JOIN MESA     m  ON m.id_mesa       = p.id_mesa
LEFT JOIN EMPLEADO e  ON e.id_empleado   = p.id_empleado
ORDER BY p.id_pedido DESC"""


def listar_pedidos():
    return SQL_LISTAR, consultar(SQL_LISTAR)


def crear_pedido(b):
    """Crea un pedido tocando 3 tablas (PEDIDO + DETALLE_PEDIDO + PRODUCTO)
    dentro de una transaccion ACID. Devuelve (pasos_sql, resultado) o lanza
    ValueError / excepcion de psycopg2 si algo falla (con ROLLBACK)."""
    items = b.get("items")
    if not isinstance(items, list) or len(items) == 0:
        raise ValueError("Debe agregar al menos un producto al pedido.")
    if not b.get("cliente_id") or not b.get("empleado_id") or not b.get("mesa_id"):
        raise ValueError("El pedido necesita cliente, mesero y mesa (son obligatorios).")

    pasos = []
    conn = get_conn()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        pasos.append("BEGIN;")

        # 1) Cabecera del pedido
        cur.execute(
            """INSERT INTO PEDIDO (id_cliente, id_empleado, id_mesa, estado, total)
               VALUES (%s, %s, %s, 'Pendiente', 0) RETURNING id_pedido""",
            [b.get("cliente_id"), b.get("empleado_id"), b.get("mesa_id")],
        )
        pedido_id = cur.fetchone()["id_pedido"]
        pasos.append(
            f"-- cabecera\nINSERT INTO PEDIDO (id_cliente, id_empleado, id_mesa, estado, total) "
            f"VALUES ({b.get('cliente_id')}, {b.get('empleado_id')}, {b.get('mesa_id')}, 'Pendiente', 0);"
        )

        # 2) Por cada item: validar stock (FOR UPDATE), insertar detalle, descontar stock
        for it in items:
            cur.execute(
                "SELECT nombre, precio, stock FROM PRODUCTO WHERE id_producto = %s FOR UPDATE",
                [it.get("producto_id")],
            )
            prod = cur.fetchone()
            if prod is None:
                raise ValueError(f"Producto {it.get('producto_id')} no existe.")
            if prod["stock"] < it.get("cantidad", 0):
                raise ValueError(
                    f'Stock insuficiente de "{prod["nombre"]}" '
                    f'(hay {prod["stock"]}, pediste {it.get("cantidad")}). Se hace ROLLBACK.'
                )

            subtotal = float(prod["precio"]) * int(it.get("cantidad"))
            cur.execute(
                """INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad, precio_unitario, subtotal)
                   VALUES (%s, %s, %s, %s, %s)""",
                [pedido_id, it.get("producto_id"), it.get("cantidad"), prod["precio"], subtotal],
            )
            pasos.append(
                f"-- linea\nINSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad, precio_unitario, subtotal) "
                f"VALUES ({pedido_id}, {it.get('producto_id')}, {it.get('cantidad')}, {prod['precio']}, {subtotal});"
            )

            cur.execute(
                "UPDATE PRODUCTO SET stock = stock - %s WHERE id_producto = %s",
                [it.get("cantidad"), it.get("producto_id")],
            )
            pasos.append(
                f"-- descontar stock\nUPDATE PRODUCTO SET stock = stock - "
                f"{it.get('cantidad')} WHERE id_producto = {it.get('producto_id')};"
            )

        # 3) Recalcular total del pedido desde el detalle
        cur.execute(
            """UPDATE PEDIDO
               SET total = (SELECT COALESCE(SUM(subtotal),0) FROM DETALLE_PEDIDO WHERE id_pedido = %s)
               WHERE id_pedido = %s""",
            [pedido_id, pedido_id],
        )
        pasos.append(
            f"-- total\nUPDATE PEDIDO SET total = (SELECT SUM(subtotal) FROM DETALLE_PEDIDO "
            f"WHERE id_pedido = {pedido_id}) WHERE id_pedido = {pedido_id};"
        )

        conn.commit()
        pasos.append("COMMIT;")

        cur.execute("SELECT total FROM PEDIDO WHERE id_pedido = %s", [pedido_id])
        total = cur.fetchone()["total"]
        cur.close()
        return "\n".join(pasos), {"id": pedido_id, "total": total}
    except Exception as e:
        conn.rollback()
        pasos.append("ROLLBACK;  -- se revierte TODO")
        msg = str(e) if isinstance(e, ValueError) else explicar_error(e)
        raise PedidoError(msg, "\n".join(pasos)) from e
    finally:
        conn.close()
