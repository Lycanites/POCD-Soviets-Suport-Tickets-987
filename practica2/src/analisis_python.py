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

# 1. Valores unicos categoricos
    set_unicos = valores_unicos(datos, col_cat)
    n_unicos = len(set_unicos)
    lista_unicos_ordenada = sorted(set_unicos)

    # 2. Conteo por categoria
    conteo = conteo_por_categoria(datos, col_cat)

    # 3. Categoria mas frecuente
    if conteo:
        cat_max = max(conteo, key=conteo.get)
        cat_mas_frecuente = {"valor": cat_max, "conteo": conteo[cat_max]}
    else:
        cat_mas_frecuente = {"valor": "N/A", "conteo": 0}

    # 4. Top 3 categorias (ordenadas de mayor a menor, desempatando alfabeticamente)
    top_3_tuplas = sorted(
        conteo.items(), key=lambda par: (-par[1], par[0])
    )[:3]
    top_3_categorias = [{"valor": val, "conteo": cnt} for val, cnt in top_3_tuplas]

    # 5. Estadisticas numericas
    stats_1 = estadisticas(datos, col_num_1)
    stats_2 = estadisticas(datos, col_num_2)

    # 6. Promedio por categoria
    prom_cat = promedio_por_categoria(datos, col_cat, col_num_1)

    # 7. Filtrado con filter y lambda usando el percentil 90
    numeros_num1 = list(
        filter(lambda x: x is not None, map(a_float, map(lambda f: f.get(col_num_1, ""), datos)))
    )
    ordenados_num1 = sorted(numeros_num1)
    n_vals = len(ordenados_num1)
    
    umbral = 0.0
    if n_vals > 0:
        pos_90 = int(0.9 * n_vals)
        pos_90 = min(pos_90, n_vals - 1)
        umbral = ordenados_num1[pos_90]

    registros_filtrados = list(
        filter(lambda fila: (a_float(fila.get(col_num_1, "")) or 0) > umbral, datos)
    )
    n_cumplen = len(registros_filtrados)
    porcentaje = round(100 * n_cumplen / n_vals, 2) if n_vals > 0 else 0.0

    # Estructura del resultado final acorde a la plantilla JSON solicitada
    resultado = {
        "archivo": archivo_csv.split("/")[-1],
        "pareja": nombre_pareja,
        "seed": seed,
        "valores_unicos_categorica": {
            "columna": col_cat,
            "n_valores_unicos": n_unicos,
            "valores": lista_unicos_ordenada,
        },
        "conteo_por_categoria": conteo,
        "categoria_mas_frecuente": cat_mas_frecuente,
        "top_3_categorias": top_3_categorias,
        "estadisticas_numerica_1": stats_1,
        "estadisticas_numerica_2": stats_2,
        "promedio_por_categoria": prom_cat,
        "filtrado": {
            "condicion": f"{col_num_1} > {umbral}",
            "umbral_usado": umbral,
            "n_registros_que_cumplen": n_cumplen,
            "porcentaje": porcentaje,
        },
    }

    # Guardar en JSON
    with open(archivo_salida, "w", encoding="utf-8") as f_salida:
        json.dump(resultado, f_salida, indent=2, ensure_ascii=False)

    print(f"¡Éxito! El archivo analisis_python.json se ha generado correctamente en: {archivo_salida}")

    if __name__ == "__main__":
        generar_analisis()