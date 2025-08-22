import pandas as pd

# Datos de ejemplo
# Un correlativo
datos_correlativos = ["000005", "000002", "000003", "000004", "000001"]
serie_correlativa = pd.Series(datos_correlativos)

# Un no correlativo
datos_no_correlativos = ["000021", "000022", "000023", "000024", "000025", "000027"]
serie_no_correlativa = pd.Series(datos_no_correlativos)


def es_correlativo_diff(serie):
    """
    Verifica si una serie es correlativa usando diferencias.
    """
    # Convertir a numérico
    serie_numerica = pd.to_numeric(serie, errors="coerce")

    # Ordenar la serie
    serie_numerica = serie_numerica.sort_values()

    # Calcular la diferencia entre elementos consecutivos
    diferencias = serie_numerica.diff()

    # Los valores de diferencia deben ser 1, excepto el primero que es NaN
    # Verificar si todos los valores (excepto el primero) son 1
    return (diferencias.iloc[1:] == 1).all()


# Probar la función
print(
    f"¿La serie correlativa es correlativa (diff)? {es_correlativo_diff(serie_correlativa)}"
)
print(
    f"¿La serie no correlativa es correlativa (diff)? {es_correlativo_diff(serie_no_correlativa)}"
)
