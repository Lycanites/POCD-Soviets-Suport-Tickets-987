import json

# Configuración inicial basada en tus datos
archivo_csv = "datos/tickets_soporte-ruido_100000.csv"
archivo_salida = "practica2/resultados/analisis_python.json"
nombre_pareja = "Rivera Vallejo Axel y Hernandez Castañeda Andre Alain"
seed = 987  # Convertido a entero para el JSON

col_cat = "categoria_problema"
col_num_1 = "tiempo_resolucion_hrs"
col_num_2 = "nivel_prioridad"  # Segunda columna numérica para estadisticas_numerica_2


def leer_csv(ruta, separador="|"):
    """Lee un archivo CSV separado por tuberias y retorna una lista de diccionarios."""
    with open(ruta, "r", encoding="utf-8") as f:
        lineas = f.read().strip().split("\n")

    cabecera = lineas[0].split(separador)
    datos = []
    for linea in lineas[1:]:
        valores = linea.split(separador)
        datos.append(dict(zip(cabecera, valores)))
    return datos


def a_float(texto):
    """Intenta convertir un texto a float; devuelve None si no es posible."""
    try:
        return float(texto)
    except (ValueError, TypeError):
        return None


def valores_unicos(datos, columna):
    """Retorna un set con los valores unicos de una columna, aplicando .strip() y sin vacios."""
    textos = map(lambda fila: fila.get(columna, "").strip(), datos)
    return set(filter(lambda v: v != "", textos))


def conteo_por_categoria(datos, columna):
    """Construye un diccionario {valor: conteo} para una columna categorica."""
    conteo = {}
    for fila in datos:
        valor = fila.get(columna, "").strip()
        if valor == "":
            continue
        conteo[valor] = conteo.get(valor, 0) + 1
    return conteo


def estadisticas(datos, columna):
    """Calcula min, max, promedio, mediana y n_valores_validos de una columna numerica."""
    # Filtrar valores no vacios y mapear a float de forma segura
    crudos = map(lambda fila: fila.get(columna, ""), datos)
    convertidos = map(a_float, crudos)
    numeros = list(filter(lambda x: x is not None, convertidos))