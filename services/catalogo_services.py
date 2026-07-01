from database import consultar

SQL_CATEGORIAS = "SELECT id_categoria AS id, nombre FROM categoria ORDER BY nombre"

SQL_CLIENTES = ("SELECT id_cliente AS id, nombre || ' ' || apellido AS nombre, email "
                "FROM cliente ORDER BY nombre")

SQL_MESAS = "SELECT id_mesa AS id, numero, capacidad, estado FROM mesa ORDER BY id_mesa"

SQL_EMPLEADOS = ("SELECT id_empleado AS id, nombre || ' ' || apellido AS nombre, rol "
                  "FROM empleado ORDER BY nombre")


def listar_categorias():
    return SQL_CATEGORIAS, consultar(SQL_CATEGORIAS)


def listar_clientes():
    return SQL_CLIENTES, consultar(SQL_CLIENTES)


def listar_mesas():
    return SQL_MESAS, consultar(SQL_MESAS)


def listar_empleados():
    return SQL_EMPLEADOS, consultar(SQL_EMPLEADOS)
