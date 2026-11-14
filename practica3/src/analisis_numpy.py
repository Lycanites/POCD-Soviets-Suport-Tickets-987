import json
import time
import numpy as np


def a_float(texto):
    """Convierte texto a float; devuelve np.nan si no se puede."""
    try:
        return float(texto.strip())
    except (ValueError, AttributeError):
        return np.nan


def cargar_columna_csv(ruta_csv, nombre_columna_objetivo):
    """Lee el CSV separado por '|', localiza la columna por nombre en la cabecera
    y devuelve el nombre, el array completo (con nan) y el array solo con valores válidos.
    """
    with open(ruta_csv, "r", encoding="utf-8") as f:
        lineas = f.read().strip().split("\n")
    
    cabecera = lineas[0].split("|")
    indice_columna = cabecera.index(nombre_columna_objetivo)
    
    crudos = []
    for linea in lineas[1:]:
        partes = linea.split("|")
        if len(partes) > indice_columna:
            crudos.append(partes[indice_columna])
            
    columna_completa = np.array([a_float(v) for v in crudos])
    columna_validos = columna_completa[~np.isnan(columna_completa)]
    
    return nombre_columna_objetivo, columna_completa, columna_validos


def calcular_resumen_estadistico(nombre_col, arr_validos):
    """Calcula los 8 estadísticos requeridos por columna, redondeados a 2 decimales."""
    return {
        "columna": nombre_col,
        "n_valores_validos": int(arr_validos.size),
        "media": float(round(arr_validos.mean(), 2)),
        "desviacion_estandar": float(round(np.std(arr_validos), 2)),  # Poblacional (ddof=0)
        "minimo": float(round(arr_validos.min(), 2)),
        "maximo": float(round(arr_validos.max(), 2)),
        "mediana": float(round(np.median(arr_validos), 2)),
        "percentil_25": float(round(np.percentile(arr_validos, 25), 2)),
        "percentil_75": float(round(np.percentile(arr_validos, 75), 2))
    }


def detectar_outliers_sigma(arr_validos, k=3):
    """Detecta outliers usando la regla de +/- k desviaciones estándar sobre valores sin redondear."""
    media = arr_validos.mean()
    std = np.std(arr_validos)
    
    limite_inf = media - k * std
    limite_sup = media + k * std
    
    mascara_outliers = (arr_validos < limite_inf) | (arr_validos > limite_sup)
    outliers = arr_validos[mascara_outliers]
    
    n_outliers = int(outliers.size)
    total_validos = arr_validos.size
    porcentaje = float(round(100 * n_outliers / total_validos, 2)) if total_validos > 0 else 0.0
    
    if n_outliers > 0:
        outliers_min = float(round(outliers.min(), 2))
        outliers_max = float(round(outliers.max(), 2))
    else:
        outliers_min = None
        outliers_max = None
        
    return {
        "metodo": f"desviacion_estandar_{k}",
        "limite_inferior": float(round(limite_inf, 2)),
        "limite_superior": float(round(limite_sup, 2)),
        "n_outliers": n_outliers,
        "porcentaje": porcentaje,
        "outliers_minimo": outliers_min,
        "outliers_maximo": outliers_max
    }


def ejecutar_benchmark(arr_validos):
    """Compara el tiempo de cálculo de media y desviación estándar (poblacional)
    entre un bucle de Python puro y NumPy vectorizado.
    """
    valores_py = arr_validos.tolist()
    n = len(valores_py)
    
    # --- Bucle de Python puro ---
    inicio = time.perf_counter()
    suma = 0.0
    for v in valores_py:
        suma += v
    media_py = suma / n

    acum = 0.0
    for v in valores_py:
        acum += (v - media_py) ** 2
    std_py = (acum / n) ** 0.5
    t_bucle = time.perf_counter() - inicio

    # --- NumPy vectorizado ---
    inicio = time.perf_counter()
    media_np = arr_validos.mean()
    std_np = arr_validos.std()
    t_numpy = time.perf_counter() - inicio

    assert np.allclose([media_py, std_py], [media_np, std_np]), "El benchmark no coincide en los cálculos."

    if t_numpy == 0.0:
        factor = None
    else:
        factor = float(round(t_bucle / t_numpy, 2))

    return {
        "n_filas": int(n),
        "tiempo_bucle_python_seg": float(round(t_bucle, 6)),
        "tiempo_numpy_seg": float(round(t_numpy, 6)),
        "factor_velocidad": factor,
        "operacion_medida": "calcular media y desviacion estandar"
    }

def main():
    # Rutas basadas estrictamente en la estructura del monorepo
    ruta_csv = "datos/tickets_soporte-ruido_100.csv"
    ruta_json = "practica3/resultados/analisis_numpy.json"
    
    archivo_tema = "tickets_soporte-ruido_100.csv"
    seed = 987

    # Nombres de las columnas numéricas para tickets_soporte
    col_1 = "tiempo_resolucion_hrs"
    col_2 = "nivel_prioridad"

    # Cargar columnas por nombre desde la cabecera
    nombre_1, _, validos_1 = cargar_columna_csv(ruta_csv, col_1)
    nombre_2, _, validos_2 = cargar_columna_csv(ruta_csv, col_2)
    
    # Calcular estadísticos
    resumen_1 = calcular_resumen_estadistico(nombre_1, validos_1)
    resumen_2 = calcular_resumen_estadistico(nombre_2, validos_2)
    
    # Detectar outliers
    outliers_1 = detectar_outliers_sigma(validos_1, k=3)
    outliers_2 = detectar_outliers_sigma(validos_2, k=3)
    
    # Benchmark sobre numerica_1
    benchmark_res = ejecutar_benchmark(validos_1)
    
    # Estructura del JSON final
    resultado_final = {
        "archivo": archivo_tema,
        "pareja": "Axel Rivera Vallejo",
        "seed": seed,
        "numerica_1": resumen_1,
        "numerica_2": resumen_2,
        "outliers_numerica_1": outliers_1,
        "outliers_numerica_2": outliers_2,
        "benchmark": benchmark_res
    }
    
    # Guardar archivo JSON
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(resultado_final, f, indent=2, ensure_ascii=False)
        
    print(f"Análisis completado exitosamente. JSON guardado en: {ruta_json}")


if __name__ == "__main__":
    main()