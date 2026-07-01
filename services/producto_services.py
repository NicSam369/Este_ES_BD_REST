import json

import psycopg2.extras

from database import get_conn, consultar

SQL_LISTAR = """SELECT p.id_producto AS id, p.nombre, p.descripcion, p.precio, p.stock,
       c.nombre AS categoria, p.id_categoria AS categoria_id, p.datos_extra AS atributos
FROM producto p
LEFT JOIN categoria c ON c.id_categoria = p.id_categoria
ORDER BY p.id_producto"""

SQL_CREAR = """INSERT INTO producto (nombre, descripcion, precio, stock, id_categoria, datos_extra)
VALUES (%s, %s, %s, %s, %s, %s::jsonb)
RETURNING id_producto AS id, nombre, descripcion, precio, stock, id_categoria, datos_extra AS atributos"""

SQL_EDITAR = """UPDATE producto
SET nombre = %s, descripcion = %s, precio = %s, stock = %s, id_categoria = %s, datos_extra = %s::jsonb
WHERE id_producto = %s
RETURNING id_producto AS id, nombre, descripcion, precio, stock, id_categoria, datos_extra AS atributos"""

SQL_BORRAR = "DELETE FROM producto WHERE id_producto = %s RETURNING id_producto AS id, nombre"


def listar_productos():
    return SQL_LISTAR, consultar(SQL_LISTAR)


def crear_producto(b):
    params = [
        b.get("nombre"),
        b.get("descripcion") or None,
        b.get("precio"),
        b.get("stock") if b.get("stock") is not None else 0,
        b.get("categoria_id") or None,
        json.dumps(b.get("atributos") or {}),
    ]
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(SQL_CREAR, params)
            row = cur.fetchone()
        conn.commit()
        return SQL_CREAR, params, row
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def editar_producto(pid, b):
    params = [b.get("nombre"), b.get("descripcion") or None, b.get("precio"),
              b.get("stock"), b.get("categoria_id") or None,
              json.dumps(b.get("atributos") or {}), pid]
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(SQL_EDITAR, params)
            row = cur.fetchone()
        conn.commit()
        return SQL_EDITAR, params, row
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def borrar_producto(pid):
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(SQL_BORRAR, [pid])
            row = cur.fetchone()
        conn.commit()
        return SQL_BORRAR, row
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
