def format_data_for_display(people):
    """
    Recibe una lista de diccionarios con las claves:
    - given_name
    - family_name
    - title

    Devuelve una lista de strings con el formato:
    "Nombre Apellido: Cargo"
    """
    return [f"{p['given_name']} {p['family_name']}: {p['title']}" for p in people]


def format_data_for_excel(people):
    """
    Recibe una lista de diccionarios con las claves:
    - given_name
    - family_name
    - title

    Devuelve un string en formato CSV con cabecera:
    given,family,title
    nombre,apellido,cargo
    """
    # Cabecera CSV
    cabecera = "given,family,title"
    # Filas con los datos de cada persona
    filas = [
        f"{p['given_name']},{p['family_name']},{p['title']}"
        for p in people
    ]
    # Unir cabecera + filas separadas por salto de línea
    return "\n".join([cabecera] + filas)
