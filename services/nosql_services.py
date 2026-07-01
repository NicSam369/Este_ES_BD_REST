from database import consultar

SQL_ETIQUETA = """SELECT id_producto AS id, nombre, precio, datos_extra AS atributos
FROM PRODUCTO
WHERE datos_extra -> 'etiquetas' ? %s"""

SQL_ALERGENO = """SELECT id_producto AS id, nombre, precio, datos_extra AS atributos
FROM PRODUCTO
WHERE datos_extra -> 'alergenos' ? %s"""


def buscar_por_etiqueta(valor):
    return consultar(SQL_ETIQUETA, [valor])


def buscar_por_alergeno(valor):
    return consultar(SQL_ALERGENO, [valor])
