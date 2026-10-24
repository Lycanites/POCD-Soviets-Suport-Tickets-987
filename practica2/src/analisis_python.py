import json

# Configuración inicial basada en tus datos
archivo_csv = "datos/tickets_soporte-ruido_100000.csv"
archivo_salida = "practica2/resultados/analisis_python.json"
nombre_pareja = "Rivera Vallejo Axel y Hernandez Castañeda Andre Alain"
seed = 987  

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
    if not numeros:
        return {
            "columna": columna,
            "n_valores_validos": 0,
            "minimo": None,
            "maximo": None,
            "promedio": None,
            "mediana": None,
        }

    ordenados = sorted(numeros)
    n = len(ordenados)

    # Calculo de la mediana (maneja casos pares e impares)
    if n % 2 == 1:
        mediana = ordenados[n // 2]
    else:
        mediana = (ordenados[(n // 2) - 1] + ordenados[n // 2]) / 2

    return {
        "columna": columna,
        "n_valores_validos": n,
        "minimo": ordenados[0],
        "maximo": ordenados[-1],
        "promedio": round(sum(ordenados) / n, 2),
        "mediana": round(mediana, 2),
    }


def promedio_por_categoria(datos, categorica, numerica):
    """Devuelve un diccionario {categoria: promedio de la columna numerica}."""
    acumulador = {}
    for fila in datos:
        cat = fila.get(categorica, "").strip()
        val_str = fila.get(numerica, "")
        val = a_float(val_str)
        if cat != "" and val is not None:
            if cat not in acumulador:
                acumulador[cat] = []
            acumulador[cat].append(val)

    promedios = {}
    for cat, lista_vals in acumulador.items():
        promedios[cat] = round(sum(lista_vals) / len(lista_vals), 2)
    return promedios