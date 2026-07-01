def explicar_error(e):
    """Traduce errores de constraints de PostgreSQL a mensajes claros en espanol."""
    code = getattr(e, "pgcode", None)
    diag = getattr(e, "diag", None)
    constraint = getattr(diag, "constraint_name", None) if diag else None
    column = getattr(diag, "column_name", None) if diag else None
    if code == "23505":
        return f"Violacion de UNIQUE: ya existe un registro con ese valor ({constraint})."
    if code == "23514":
        return f"Violacion de CHECK: el valor no cumple la regla ({constraint})."
    if code == "23502":
        return f'Violacion de NOT NULL: el campo "{column}" es obligatorio.'
    if code == "23503":
        return (f"Violacion de llave foranea: el registro relacionado no existe "
                f"o no se puede borrar ({constraint}).")
    return str(e).splitlines()[0] if str(e) else "Error desconocido."
