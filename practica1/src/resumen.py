
archivo_csv = "datos/tickets_soporte-ruido_100.csv"  # probar con el de 100 primero y despues coambiar al de 100,000
archivo_salida = "practica1/resultados/resumen.txt"

# Datos informativos para el reporte
nombre_pareja = "Rivera Vallejo Axel y Hernandez Castañeda Andre"
seed = "987"

# Columnas clave según tu tema asignado (tickets_soporte)
col_cat = "categoria_problema"
col_num = "tiempo_resolucion_hrs"

def procesar_dataset():
    print("Leyendo y procesando el archivo (esto puede tomar unos segundos)...")
    
    # Leer el archivo directamente
    with open(archivo_csv, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    if not lineas:
        print("El archivo está vacío.")
        return

    # Leer encabezados y contar columnas
    encabezado_linea = lineas[0].rstrip("\n\r")
    columnas = encabezado_linea.split("|")
    n_columnas = len(columnas)

    # Obtener índices de las columnas objetivo
    idx_cat = columnas.index(col_cat)
    idx_num = columnas.index(col_num)

    filas_datos = []
    n_filas = 0
    
    frecuencia_cat = {}
    valores_num = []
    
    celdas_vacias_totales = 0
    celdas_vacias_por_columna = {col: 0 for col in columnas}

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
        frecuencia_cat[val_cat] = frecuencia_cat.get(val_cat, 0) + 1
    # 5. Análisis de la columna numérica
    val_num_str = valores[idx_num].strip() if idx_num < len(valores) else ""
    if val_num_str != "":
        try:
            num_val = float(val_num_str)
            valores_num.append(num_val)
        except ValueError:
            pass