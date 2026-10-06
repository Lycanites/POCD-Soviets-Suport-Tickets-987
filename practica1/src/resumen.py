# Configuración de rutas mediante texto plano
archivo_csv = "datos/tickets_soporte-ruido_100.csv"  # cambiar al de 1000
archivo_salida = "practica1/resultados/resumen.txt"

# Datos informativos para el reporte
nombre_pareja = "Rivera Vallejo Axel y Hernandez Castañeda Andre Alain"
seed = "987"

# Columnas clave según tu tema asignado (tickets_soporte)
col_cat = "categoria_problema"
col_num = "tiempo_resolucion_hrs"

def generar_resumen(ruta_csv, col_categorica, col_numerica, ruta_salida):
    print(f"Leyendo el archivo: {ruta_csv}...")    
    
    # Leer el archivo directamente
    with open(ruta_csv, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    if not lineas:
        print("El archivo está vacío.")
        return

    # 1. Leer encabezados y contar columnas
    encabezado_linea = lineas[0].rstrip("\n\r")
    columnas = encabezado_linea.split("|")
    n_columnas = len(columnas)

    # Obtener índices de las columnas objetivo
    idx_cat = columnas.index(col_categorica)
    idx_num = columnas.index(col_numerica)

    filas_datos = []
    n_filas = 0
    
    frecuencia_cat = {}
    valores_num = []
    
    celdas_vacias_totales = 0
    celdas_vacias_por_columna = {}
    for c in columnas:
        celdas_vacias_por_columna[c] = 0

    # 2. Recorrer línea por línea excluyendo la cabecera
    for linea in lineas[1:]:
        linea_limpia = linea.rstrip("\n\r")
        if not linea_limpia.strip():
            continue
            
        valores = linea_limpia.split("|")
        n_filas += 1
        filas_datos.append(valores)

        # 3. Evaluar calidad de datos (celdas vacías)
        for i, col_nombre in enumerate(columnas):
            val = valores[i] if i < len(valores) else ""
            if val.strip() == "":
                celdas_vacias_totales += 1
                celdas_vacias_por_columna[col_nombre] += 1

        # 4. Análisis de la columna categórica
        val_cat = valores[idx_cat].strip() if idx_cat < len(valores) else ""
        if val_cat != "":
            if val_cat in frecuencia_cat:
                frecuencia_cat[val_cat] = frecuencia_cat[val_cat] + 1
            else:
                frecuencia_cat[val_cat] = 1

        # 5. Análisis de la columna numérica
        val_num_str = valores[idx_num].strip() if idx_num < len(valores) else ""
        if val_num_str != "":
            try:
                num_val = float(val_num_str)
                valores_num.append(num_val)
            except ValueError:
                pass

    # Calcular estadísticas categóricas
    n_unicos_cat = len(frecuencia_cat)
    val_mas_frecuente = "N/A"
    conteo_mas_frecuente = 0
    for categoria in frecuencia_cat:
        if frecuencia_cat[categoria] > conteo_mas_frecuente:
            conteo_mas_frecuente = frecuencia_cat[categoria]
            val_mas_frecuente = categoria

    # Calcular estadísticas numéricas
    n_validos_num = len(valores_num)
    min_num = "N/A"
    max_num = "N/A"
    if len(valores_num) > 0:
        min_num = valores_num[0]
        max_num = valores_num[0]
        for val in valores_num:
            if val < min_num:
                min_num = val
            if val > max_num:
                max_num = val

    # Obtener las primeras 5 filas para el reporte
    primeras_5 = filas_datos[:5]

    # Extraer solo el nombre del archivo CSV (ej. tickets_soporte-ruido_100000.csv) sin la ruta de carpetas
    partes_ruta = ruta_csv.split("/")
    nombre_archivo_csv = partes_ruta[-1]

    # 6. Escribir el reporte completo usando f.write() respetando toda la plantilla
    with open(ruta_salida, "w", encoding="utf-8") as f_salida:
        f_salida.write("=== RESUMEN DEL DATASET ===\n")
        f_salida.write(f"Archivo: {nombre_archivo_csv}\n")
        f_salida.write(f"Pareja: {nombre_pareja}\n")
        f_salida.write(f"Seed: {seed}\n\n")
        
        f_salida.write("--- Dimensiones ---\n")
        f_salida.write(f"Filas: {n_filas}\n")
        f_salida.write(f"Columnas: {n_columnas}\n")
        f_salida.write(f"Nombres de columnas: {', '.join(columnas)}\n\n")
        
        f_salida.write("--- Primeras 5 filas ---\n")
        f_salida.write(" | ".join(columnas) + "\n")
        for fila in primeras_5:
            f_salida.write(" | ".join(fila) + "\n")
        f_salida.write("\n")
        
        f_salida.write(f"--- Columna categórica: {col_categorica} ---\n")
        f_salida.write(f"Valores únicos: {n_unicos_cat}\n")
        f_salida.write(f"Valor más frecuente: {val_mas_frecuente} ({conteo_mas_frecuente} apariciones)\n\n")
        
        f_salida.write(f"--- Columna numérica: {col_numerica} ---\n")
        f_salida.write(f"Valores válidos (no vacíos): {n_validos_num}\n")
        f_salida.write(f"Mínimo: {min_num}\n")
        f_salida.write(f"Máximo: {max_num}\n\n")
        
        f_salida.write("--- Calidad de datos ---\n")
        f_salida.write(f"Celdas vacías totales: {celdas_vacias_totales}\n")
        f_salida.write("Celdas vacías por columna:\n")
        for col_nombre in columnas:
            cant_vacias = celdas_vacias_por_columna[col_nombre]
            f_salida.write(f"  {col_nombre}: {cant_vacias}\n")

    print(f"¡Éxito! El archivo resumen.txt se ha generado correctamente en: {ruta_salida}")

if __name__ == "__main__":
    generar_resumen(
        ruta_csv=archivo_csv,
        col_categorica=col_cat,
        col_numerica=col_num,
        ruta_salida=archivo_salida
    )